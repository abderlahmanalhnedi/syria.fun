import { localized, t, number } from './i18n.js';
import { read, write } from './storage.js';
import { element, url } from './dom.js';
export function initializeQuizzes(quizzes) {
  const panel = document.querySelector('#quiz-panel');
  if (!panel) return;
  const selection = document.querySelector('#quiz-selection');
  let active = null;
  let index = 0;
  let score = 0;
  let answer = null;
  let finished = false;
  function best(id) {
    const value = read(`score.${id}`, 0);
    return Number.isInteger(value) && value >= 0 && value <= 5 ? value : 0;
  }
  function updateBest() {
    document.querySelectorAll('[data-best]').forEach(node => { node.textContent = `${t('best')}: ${number(best(node.dataset.best))} / ${number(5)}`; });
  }
  function button(label, className, callback) {
    const node = element('button', className, label);
    node.type = 'button';
    node.addEventListener('click', callback);
    return node;
  }
  function exitQuiz() {
    const id = active?.id;
    active = null;
    panel.hidden = true;
    selection.hidden = false;
    document.querySelector(`[data-start-quiz="${id}"]`)?.focus();
    const address = new URL(location.href);
    address.searchParams.delete('quiz');
    history.replaceState(null, '', address);
    updateBest();
  }
  function render(focus = true) {
    if (!active) { updateBest(); return; }
    panel.replaceChildren();
    const heading = element('h2', 'quiz-name', localized(active.name));
    const meta = element('div', 'quiz-meta');
    meta.append(element('span', '', finished ? t('quizScore') : `${t('question')} ${number(index+1)} ${t('of')} ${number(active.questions.length)}`), button(t('endQuiz'), 'text-button', exitQuiz));
    panel.append(heading, meta);
    if (finished) {
      const resultHeading = element('h3', 'quiz-question', t('resultTitle'));
      resultHeading.tabIndex = -1;
      const resultScore = element('p', 'result-score', `${number(score)} / ${number(active.questions.length)}`);
      const actions = element('div', 'button-row');
      actions.append(button(t('restart'), 'button primary', () => start(active.id)), button(t('allQuizzes'), 'button secondary', exitQuiz));
      panel.append(resultHeading, resultScore, element('p', '', t('resultIntro')), element('p', 'best-score', `${t('best')}: ${number(best(active.id))} / ${number(5)}`), actions);
      if (focus) resultHeading.focus();
      return;
    }
    const progress = element('progress', 'quiz-progress');
    progress.max = active.questions.length;
    progress.value = index + (answer === null ? 0 : 1);
    progress.setAttribute('aria-label', `${t('question')} ${number(index+1)} ${t('of')} ${number(active.questions.length)}`);
    panel.append(progress);
    const question = active.questions[index];
    const prompt = element('h3', 'quiz-question', localized(question.prompt));
    prompt.tabIndex = -1;
    const options = element('div', 'quiz-options');
    options.setAttribute('role', 'group');
    options.setAttribute('aria-label', localized(question.prompt));
    localized(question.options).forEach((text, optionIndex) => {
      const choice = button(text, 'quiz-option', () => {
        if (answer !== null) return;
        answer = optionIndex;
        if (answer === question.answer) score++;
        render(false);
        panel.querySelector('.quiz-feedback').focus();
      });
      choice.dataset.option = optionIndex;
      if (answer !== null) {
        choice.disabled = true;
        if (optionIndex === question.answer) { choice.classList.add('correct'); choice.append(element('span', 'answer-mark', '✓')); }
        else if (optionIndex === answer) { choice.classList.add('incorrect'); choice.append(element('span', 'answer-mark', '×')); }
      }
      options.append(choice);
    });
    panel.append(prompt, options);
    if (answer !== null) {
      const feedback = element('div', 'quiz-feedback');
      feedback.tabIndex = -1;
      feedback.setAttribute('role', 'status');
      feedback.append(element('strong', '', t(answer === question.answer ? 'correct' : 'incorrect')), element('p', '', `${t('correctAnswer')}: ${localized(question.options)[question.answer]}. ${localized(question.explanation)}`));
      const reference = element('a', 'text-link', t('source'));
      reference.href = question.source;
      feedback.append(reference);
      const last = index === active.questions.length-1;
      panel.append(feedback, button(t(last ? 'showResult' : 'next'), 'button primary quiz-next', () => {
        if (last) { finished = true; write(`score.${active.id}`, Math.max(best(active.id), score)); updateBest(); }
        else { index++; answer = null; }
        render();
      }));
    }
    if (focus) prompt.focus();
  }
  function start(id) {
    active = quizzes.find(quiz => quiz.id === id);
    if (!active) return;
    index = score = 0;
    answer = null;
    finished = false;
    selection.hidden = true;
    panel.hidden = false;
    const address = new URL(location.href);
    address.searchParams.set('quiz', id);
    history.replaceState(null, '', address);
    render();
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  document.querySelectorAll('[data-start-quiz]').forEach(node => node.addEventListener('click', () => start(node.dataset.startQuiz)));
  document.addEventListener('language-change', () => render(false));
  updateBest();
  const initial = new URLSearchParams(location.search).get('quiz');
  if (initial) start(initial);
}
