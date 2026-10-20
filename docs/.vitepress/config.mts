import { defineConfig } from 'vitepress'
export default defineConfig({
  lang: 'uk-UA',
  title: 'JS Нотатки',
  description: 'Нотатки для підготовки до співбесіди з JavaScript',
  base: process.env.BASE || '/js-interview-notes/',
  appearance: 'dark',
  cleanUrls: true,
  lastUpdated: false,
  markdown: { theme: { light: 'github-light', dark: 'github-dark' } },
  themeConfig: {
    nav: [{ text: 'Чекліст', link: '/checklist' }],
    sidebar: [
      { text: 'Об’єкти та прототипи', items: [
        { text: '[[Prototype]] і __proto__', link: '/objects/prototype' },
        { text: 'Гетери і сетери', link: '/objects/getters-setters' },
        { text: 'preventExtensions, seal, freeze', link: '/objects/freeze-seal' },
        { text: 'Proxy та Reflect', link: '/objects/proxy-reflect' } ] },
      { text: 'Функції', items: [
        { text: 'Замикання', link: '/functions/closures' },
        { text: 'Throttle', link: '/functions/throttle' } ] },
      { text: 'Асинхронність', items: [
        { text: 'async / await', link: '/async/async-await' },
        { text: 'Промісифікація', link: '/async/promisification' } ] },
      { text: 'Браузерні API', items: [
        { text: 'async і defer', link: '/browser/async-defer' },
        { text: 'MutationObserver', link: '/browser/mutation-observer' },
        { text: 'WebSocket, SSE, Workers', link: '/browser/websocket-sse-workers' },
        { text: 'WebSocket у Vue 3 та React', link: '/browser/websocket-vue-react' } ] },
      { text: 'Чекліст', items: [{ text: 'Interview Prep Checklist', link: '/checklist' }] },
    ],
    outline: { level: [2, 3], label: 'На цій сторінці' },
    docFooter: { prev: 'Попередня', next: 'Наступна' },
    darkModeSwitchLabel: 'Тема', lightModeSwitchTitle: 'Світла тема', darkModeSwitchTitle: 'Темна тема',
    sidebarMenuLabel: 'Меню', returnToTopLabel: 'Нагору',
    notFound: { title: 'СТОРІНКУ НЕ ЗНАЙДЕНО', quote: 'Такої сторінки немає.', linkText: 'На головну' },
    search: { provider: 'local', options: { translations: {
      button: { buttonText: 'Пошук', buttonAriaLabel: 'Пошук' },
      modal: { noResultsText: 'Нічого не знайдено', resetButtonTitle: 'Очистити', backButtonTitle: 'Закрити',
        displayDetails: 'Детальний список',
        footer: { selectText: 'вибрати', navigateText: 'навігація', closeText: 'закрити' } } } } },
  },
})
