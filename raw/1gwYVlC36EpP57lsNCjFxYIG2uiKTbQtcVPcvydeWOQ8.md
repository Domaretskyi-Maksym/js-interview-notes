# \# WebSocket у Vue 3 та React

Конспект: де підключатись, як тримати стан, reconnect, heartbeat, cleanup. Браузерний API однаковий у всіх фреймворках.

\---

## \#\# 1\. Що таке WebSocket

\- **\*\*Дупlex:\*\*** сервер і клієnt можуть слати дані в будь-який момент.  
\- **\*\*Handshake:\*\*** один раз HTTP **\*\*Upgrade\*\*** (\`101 Switching Protocols\`), далі — фрейми WS, не REST.  
\- У коді чату handshake **\*\*не пишуть\*\*** — його роблять \`new WebSocket(url)\` і сервер (наприклад \`ws\` у Node).  
\- Після успіху: **\*\*\`onopen\`\*\*** (клієnt) / \`connection\` (сервер).  
\- Перевірка: DevTools → Network → **\*\*WS\*\*** → Headers (101) \+ Messages.

`| REST | WebSocket |`  
`|------|-----------|`  
`| Request → response | Довгоживе з’єднання |`  
`| Сервер не push’ить сам | Server push |`  
`| Кожен запит — нове з’єднання (зазвичай) | Один канал |`

\---

## \#\# 2\. Browser API

```` ```text ````  
`new WebSocket('ws://host' | 'wss://host')`  
`ws.send(string)                    // об’єкт → JSON.stringify`  
`ws.close()`

`ws.readyState: CONNECTING(0) | OPEN(1) | CLOSING(2) | CLOSED(3)`

`ws.onopen | onmessage | onclose | onerror`  
`onmessage → event.data (string)`  
```` ``` ````

**\*\*Prod:\*\*** завжди **\*\*\`wss://\`\*\*** за HTTPS. Auth: query \`?token=\`, cookie, або перший кадр \`{ type: 'auth' }\`.

\---

## \#\# 3\. Де що робити (архітектура)

`| Що | Де |`  
`|----|-----|`  
``| Екземпляр `WebSocket` | Поза UI: `let ws` (Vue) / `useRef` (React) |``  
``| Статус, messages, ціна | `ref` / `useState` |``  
``| Підключення | Функція **`connect()`** |``  
``| Reconnect | **`onclose`** (+ backoff), не в `onerror` окремо |``  
``| Heartbeat start | **`onopen`** |``  
``| Heartbeat stop + reconnect timers | **`onclose`**, **unmount cleanup** |``  
``| Навмисний вихід | **`disconnect()`** + прапорець «не reconnect» |``

**\*\*Один власник\*\*** сокета на фічу: composable, hook, store — не кілька компонентів з окремими WS на той самий чат.

**\*\*Не роби\*\*** \`new WebSocket\` при import модуля — лише mount / \`connect()\`.

\---

## \#\# 4\. Vue 3

### \#\#\# Lifecycle

```` ```text ````  
`onMounted  → connect()`  
`onUnmounted → isUnmounting = true → clear timers → ws.close()`  
```` ``` ````

Composable може викликати \`onScopeDispose(disconnect)\` або view сам викликає \`onUnmounted(disconnect)\`.

### \#\#\# Патерн у компоненті

\- \`let ws: WebSocket | null \= null\`  
\- \`const status \= ref\<...\>('connecting')\`  
\- У \`onmessage\` оновлюй \`ref\` через \`.value\`  
\- Сокет **\*\*не\*\*** в \`ref\`, якщо не потрібен у template

### \#\#\# Composable (Рівень 4\)

Файл: \`src/composables/useWebSocket.ts\`

Повертає:

\- \`status\`, \`messages\`, \`reconnectAttempt\`, \`nextDelayMs\`, \`lastPongAt\`  
\- \`connect()\`, \`disconnect()\`, \`send()\`

View лишається UI \+ \`onMounted(connect)\` / \`onUnmounted(disconnect)\`.

### \#\#\# Pinia (опційно)

Глобальний чат: \`connect\` / \`disconnect\` у store actions; cleanup при logout.

\---

## \#\# 5\. React

### \#\#\# Lifecycle

```` ```text ````  
`useEffect(() => {`  
 `connect()`  
 `return () => disconnect()   // = onUnmounted`  
`}, [url])                       // зміна url → cleanup → новий connect`  
```` ``` ````

**\*\*Strict Mode (dev):\*\*** effect двічі mount/cleanup — cleanup має бути коректним.

### \#\#\# Патерн

\- Сокет: **\*\*\`useRef\<WebSocket | null\>(null)\`\*\*** — не \`useState\`  
\- Статус / messages: **\*\*\`useState\`\*\***  
\- У \`onmessage\`: **\*\*\`setMessages(prev \=\> \[...prev, text\])\`\*\*** — інакше stale closure  
\- Cleanup у **\*\*\`return\`\*\*** effect — те саме, що Vue \`onUnmounted\`

### \#\#\# Custom hook

\`hooks/useWebSocket.ts\` — той самий контракт, що Vue composable. Шаблон: \`practice/templates/useWebSocket.react.ts\`.

\---

## \#\# 6\. Функція \`connect()\`

Один раз зібрати:

1\. \`status \= 'connecting'\`  
2\. \`ws \= new WebSocket(url)\`  
3\. \`onopen\` — open, скинути backoff, **\*\*startHeartbeat()\*\***  
4\. \`onmessage\` — parse за \`type\`  
5\. \`onclose\` — **\*\*stopHeartbeat()\*\***, якщо не unmount → **\*\*scheduleReconnect()\*\***  
6\. \`onerror\` — error (часто далі буде \`onclose\`)

Перший виклик: mount. Після обриву: **\*\*\`setTimeout(connect, delay)\`\*\*** — **\*\*новий\*\*** \`WebSocket\`.

\---

## \#\# 7\. Reconnect \+ exponential backoff

**\*\*Тригер:\*\*** \`onclose\` (сервер упав, мережа, heartbeat викликав \`close()\`).

**\*\*Не reconnect:\*\***

\- користувач покинув сторінку (\`isUnmounting\` / cleanup effect)  
\- logout / навмисний \`disconnect()\`

**\*\*Backoff:\*\*** 1s → 2s → 4s → 8s (cap). На **\*\*\`onopen\`:\*\*** \`attempt \= 0\`.

**\*\*Jitter у prod:\*\*** \`delay \+ random(0, n)\` — менше «шторму» на сервер.

Зберігай **\*\*id\*\*** \`setTimeout\`, **\*\*clear\*\*** перед новим schedule і в cleanup.

**\#\#\# Vue: unmount**

```` ```text ````  
`onUnmounted:`  
 `isUnmounting = true    // ПЕРЕД ws.close()`  
 `clearTimeout(reconnectId)`  
 `stopHeartbeat()`  
 `ws?.close()`  
```` ``` ````

Інакше \`onclose\` запланує reconnect без компонента.

\---

## \#\# 8\. Heartbeat (application-level)

Навіщо: перевірити, що **\*\*сервер обробляє\*\*** повідомлення, не лише TCP.

`| Крок | Дія |`  
`|------|-----|`  
``| Кожні N s (навчання: 5) | `send(JSON.stringify({ type: 'ping' }))` |``  
``| Після ping | watchdog 3s: нема `{ type: 'pong' }` → **`ws.close()`** |``  
``| `pong` у onmessage | оновити `lastPongAt`, clear watchdog, **не в чат** |``  
``| Start | **`onopen`** |``  
``| Stop | **`onclose`**, unmount |``

Не стартуй interval у mount без \`onopen\` — після reconnect буде кілька interval.

На рівні протоколу WS теж є ping/pong; app-level ping — для перевірки backend.

\---

## \#\# 9\. Протокол поверх WS

Кадри з полем **\*\*\`type\`:\*\***

`| type | Дія |`  
`|------|-----|`  
``| `system` | Системний текст у UI |``  
``| `message` | Чат |``  
``| `ping` / `pong` | Heartbeat |``  
``| `auth` | (prod) токен |``

Один парсер у \`onmessage\`, гілки за \`type\`. \`send\` — string або \`JSON.stringify\`.

\---

## \#\# 10\. Потоки даних (ticker)

\- **\*\*Не\*\*** накопичувати всі кадри в масив у state.  
\- Тримати **\*\*останню\*\*** ціну \+ попередню для trend.  
\- Опційно: **\*\*throttle\*\*** / \`requestAnimationFrame\` для UI.  
\- **\*\*\`onUnmounted\` / effect cleanup\*\*** → \`close()\`.

Приклад: Binance \`wss://stream.binance.com:9443/ws/btcusdt@trade\`, поле **\*\*\`p\`\*\***.

\---

## \#\# 11\. Типові помилки

1\. Нема **\*\*\`close()\`\*\*** на unmount → leak.  
2\. Reconnect у \`onclose\` без **\*\*\`isUnmounting\`\*\*** → reconnect після exit.  
3\. Не **\*\*clear\*\*** interval/timeout → подвоєння після reconnect.  
4\. **\*\*\`send\` до \`onopen\`\*\*** — перевіряй \`readyState \=== OPEN\`.  
5\. Сокет у **\*\*\`useState\` / reactive\*\*** без потреби.  
6\. Порівняння цін як **\*\*рядки\*\*** — використовуй **\*\*number\*\***.  
7\. \`catch (e: Error)\` у TS — лише \`unknown\` або без типу.

\---

## \#\# 12\. Vue vs React (шпаргалка)

`| | Vue 3 | React |`  
`|---|--------|--------|`  
``| Старт | `onMounted` | `useEffect` |``  
``| Стоп | `onUnmounted` | effect `return` |``  
``| Сокет | `let ws` | `useRef` |``  
``| UI state | `ref` | `useState` |``  
`| Спільна логіка | **composable** | **custom hook** |`  
``| Оновлення в callback | `messages.value = …` | `setState(prev => …)` |``

\---

## \#\# 13\. Прод (коротко)

\- \`wss://\`, auth, shared TS-контракт client/server  
\- Backoff \+ jitter, max attempts, **\*\*resubscribe / resync\*\*** після reconnect (REST для історії)  
\- Черга \`send\`, поки не OPEN  
\- SDK (Socket.IO, Ably, …) або власний composable/hook  
\- Heartbeat рідше (30–60s) \+ моніторинг

\---

## \#\# 14\. Локальна практика в цьому репо

`| Рівень | Route | Фокус |`  
`|--------|--------|--------|`  
``| 1 | `/practice/ws/level-1` | API, чат |``  
``| 2 | `/practice/ws/level-2` | Binance stream |``  
``| 3 | `/practice/ws/level-3` | reconnect + heartbeat |``  
``| 4 | `src/composables/useWebSocket.ts` | винести логіку |``

Сервер чату: \`npm run ws:server\` → \`ws://localhost:8080\` (ping → pong).

\---

## \#\# 15\. Відповідь на інтерв’ю (одним абзацом)

*\*WebSocket тримаю поза render tree — ref у React, змінна або composable у Vue. Підключення через \`connect()\` після mount; reconnect у \`onclose\` з exponential backoff; на unmount — прапорець, clear timers, \`close()\`, без reconnect. Heartbeat стартую в \`onopen\`, зупиняю на close/unmount. UI отримує status і data через composable або hook; протокол — typed messages поверх WS.\**

