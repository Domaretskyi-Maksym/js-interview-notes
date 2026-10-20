* # async / await

* **Що робить ключове слово `async` перед функцією?** Воно гарантує дві речі: функція завжди повертатиме `Promise` (навіть якщо ви повертаєте звичайне число, воно автоматично загорнеться в успішно виконаний проміс), і всередині цієї функції дозволяється використовувати ключове слово `await`.  
* **Як працює `await` "під капотом"?** Він призупиняє виконання поточної функції доти, поки проміс не перейде у стан `settled` (виконано або відхилено). При цьому `await` не блокує весь потік виконання програми (інші події, таймери чи скрипти продовжують працювати), він лише "ставить на паузу" конкретну `async`\-функцію.  
* **Як правильно обробляти помилки при використанні** `async/await`**?** Оскільки `await` у разі відхилення промісу генерує виняток (ніби спрацював оператор `throw`), для перехоплення помилок використовується класичний синхронний блок `try..catch` навколо викликів `await`.  
* **Що буде, якщо використати `await` у звичайній (не `async`) функції?** Виникне синтаксична помилка (`SyntaxError`). `await` працює виключно всередині `async`\-функцій або на найвищому рівні (top-level) у сучасних ES-модулях.

## Практичне завдання: "Рефакторинг на сучасний лад"

На співбесідах дуже люблять давати старий ланцюжок `.then().catch()` і просити переписати його на чистий `async/await`.

Перепишіть функцію `loadData`, зберігши логіку успішного отримання даних та перехоплення помилок.

`JavaScript`

```
function loadData() {
  return fetch('https://jsonplaceholder.typicode.com/users/1')
    .then(response => {
      if (!response.ok) {
        throw new Error("Помилка мережі");
      }
      return response.json();
    })
    .then(user => {
      console.log("Отримано користувача:", user.name);
      return user;
    })
    .catch(error => {
      console.log("Сталася помилка:", error.message);
    });
}

loadData();
```

`sync function loadData() {`  
 `try {`  
   `const response = await fetch('https://jsonplaceholder.typicode.com/users/1')`  
   `if (!response.ok) {`  
       `throw new Error("Помилка мережі");`  
     `}`  
   `let user = await response.json();`  
   `console.log("Отримано користувача:", user.name);`  
   `return user;`  
 `} catch(error) {`  
   `console.log("Сталася помилка:", error.message);`  
 `}`  
`JavaScript`

```
function loadData() {
  return fetch('https://jsonplaceholder.typicode.com/users/1')
    .then(response => {
      if (!response.ok) {
        throw new Error("Помилка мережі");
      }
      return response.json();
    })
    .then(user => {
      console.log("Отримано користувача:", user.name);
      return user;
    })
    .catch(error => {
      console.log("Сталася помилка:", error.message);
    });
}

loadData();
```

`sync function loadData() {`  
 `try {`  
   `const response = await fetch('https://jsonplaceholder.typicode.com/users/1')`  
   `if (!response.ok) {`  
       `throw new Error("Помилка мережі");`  
     `}`  
   `let user = await response.json();`  
   `console.log("Отримано користувача:", user.name);`  
   `return user;`  
 `} catch(error) {`  
   `console.log("Сталася помилка:", error.message);`  
 `}`  
`}`  
