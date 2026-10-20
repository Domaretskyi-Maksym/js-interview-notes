# Throttle

## Проблема базової реалізації (через `Date.now()`)

* **Втрата останнього виклику:** Базовий підхід ігнорує всі виклики під час "заморозки". Якщо останній виклик (наприклад, фінальна координата зупинки миші) припадає на період паузи, він втрачається назавжди.

**Ідеальне рішення (рівень Senior)** Справжній `throttle` (як у Lodash) виконує перший виклик миттєво. Якщо під час паузи надходять нові виклики, він запам'ятовує контекст та аргументи останнього з них і гарантовано виконує його після завершення таймера.

### Готовий код для співбесіди:

`JavaScript`

```
function throttle(fn, wait) {
  let isThrottled = false;
  let savedArgs, savedThis;

  function wrapper(...args) {
    if (isThrottled) {
      // Пауза триває: запам'ятовуємо останні аргументи і контекст
      savedArgs = args;
      savedThis = this;
      return;
    }

    // Перший виклик проходить миттєво
    fn.apply(this, args);
    isThrottled = true;

    // Встановлюємо таймер паузи
    setTimeout(function() {
      isThrottled = false;
      // Після паузи виконуємо останній збережений виклик (якщо він був)
      if (savedArgs) {
        wrapper.apply(savedThis, savedArgs);
        savedArgs = savedThis = null; // Очищаємо пам'ять
      }
    }, wait);
  }

  return wrapper;
}
```

