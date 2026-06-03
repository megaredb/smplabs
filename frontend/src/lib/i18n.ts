import { register, init, getLocaleFromNavigator } from 'svelte-i18n';
import { browser } from '$app/environment';

// Реєструємо мови
register('en', () => import('$lib/messages/en.json'));
register('uk', () => import('$lib/messages/uk.json'));

init({
  fallbackLocale: 'en',
  // Перевіряємо, чи ми в браузері
  initialLocale: browser ? window.navigator.language : 'en', 
});