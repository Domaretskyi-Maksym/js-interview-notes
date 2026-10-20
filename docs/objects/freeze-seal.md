# preventExtensions, seal, freeze

::: v-pre
**Дескриптори властивостей** працюють на рівні окремих властивостей.

Методи `Object.preventExtensions`, `Object.seal` і `Object.freeze` обмежують доступ до **всього об’єкта**.

## 1\. Object.preventExtensions(obj)

Забороняє **додавання** нових властивостей.

Існуючі властивості можна змінювати і видаляти.


```js
const obj = { a: 1 };

Object.preventExtensions(obj);

obj.a = 10;        // працює
obj.b = 2;         // не працює (у strict mode — помилка)
delete obj.a;      // працює

console.log(obj);  // { a: 10 }
```

**Перевірка:**


```js
Object.isExtensible(obj); // false
```

---

## 2\. Object.seal(obj)

* Забороняє додавання **і** видалення властивостей.  
* Для всіх існуючих властивостей встановлює `configurable: false`.  
* Значення властивостей **можна** змінювати (якщо вони `writable: true`).


```js
const obj = { a: 1, b: 2 };

Object.seal(obj);

obj.a = 10;        // працює
obj.c = 3;         // не працює
delete obj.b;      // не працює

console.log(obj);  // { a: 10, b: 2 }
```

**Перевірка:**


```js
Object.isSealed(obj); // true
```

---

## 3\. Object.freeze(obj)

**Найжорсткіше обмеження:**

* Забороняє додавання, видалення **і** зміну властивостей.  
* Встановлює `configurable: false` і `writable: false` для всіх існуючих властивостей.


```js
const obj = { a: 1, b: 2 };

Object.freeze(obj);

obj.a = 10;        // не працює
obj.c = 3;         // не працює
delete obj.b;      // не працює

console.log(obj);  // { a: 1, b: 2 }
```

**Перевірка:**


```js
Object.isFrozen(obj); // true
```

---

## Порівняльна таблиця

| Метод | Додавання | Видалення | Зміна значення | configurable | writable |
| ----- | ----- | ----- | ----- | ----- | ----- |
| preventExtensions | ❌ | ✅ | ✅ | не змінює | не змінює |
| seal | ❌ | ❌ | ✅ | false | не змінює |
| freeze | ❌ | ❌ | ❌ | false | false |

---

## Важливі зауваження

1. **Усі ці методи працюють лише на верхньому рівні** (shallow).  
   Вкладені об’єкти залишаються звичайними:  

```js
const obj = {
  nested: { x: 1 }
};
Object.freeze(obj);

obj.nested.x = 99; // працює!
```

3. У **strict mode** спроби порушити обмеження викликають `TypeError`.  
   У звичайному режимі операції просто ігноруються.  
4. Методи повертають той самий об’єкт, тому їх можна використовувати ланцюжком:  

```js
const frozen = Object.freeze({ a: 1 });
```

6. Перевірочні методи:  
   * `Object.isExtensible(obj)` → false, якщо додавання заборонено  
   * `Object.isSealed(obj)` → true, якщо додавання/видалення заборонено і всі властивості `configurable: false`  
   * `Object.isFrozen(obj)` → true, якщо додавання/видалення/зміна заборонені і всі властивості `configurable: false` \+ `writable: false`

Це класичний інструментарій JavaScript для створення «захищених» об’єктів.

:::
