import { register, init } from 'svelte-i18n';
import { browser } from '$app/environment';

// Реєструємо мови
register('en', () => import('$lib/messages/en.json'));
register('uk', () => import('$lib/messages/uk.json'));

// Функція для читання cookie
function getSavedLocale() {
	if (!browser) return null;
	const match = document.cookie.match(new RegExp('(^| )locale=([^;]+)'));
	return match ? match[2] : null;
}

init({
	fallbackLocale: 'en',
	// Спочатку шукаємо в cookie, якщо немає — беремо мову браузера
	initialLocale: getSavedLocale() || (browser ? window.navigator.language : 'en')
});
