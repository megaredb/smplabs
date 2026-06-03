<script lang="ts">
	import '$lib/i18n';
	import { isLoading, _, locale } from 'svelte-i18n';
	import './app.css';
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import { browser } from '$app/environment';
	import { Button } from '$lib/components/ui/button';
	import { resolve } from '$app/paths';
	import { createCreateVisitApiV1VisitsPost } from '$lib/api/generated/endpoints';

	let { children } = $props();

	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				enabled: browser,
				retry: false
			}
		}
	});

	let isLoggedIn = $state(false);
	let currentUserId = $state<number | null>(null);
	let isMounted = $state(false);

	onMount(() => {
		isMounted = true;
		const token = localStorage.getItem('access_token');
		if (token) {
			isLoggedIn = true;
			try {
				const payload = JSON.parse(atob(token.split('.')[1]));
				currentUserId = parseInt(payload.sub);
			} catch {}
		}

		// Підключення до WebSockets для нотифікацій
		const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		const wsUrl = `${protocol}//${window.location.host}/ws/notifications`;
		const ws = new WebSocket(wsUrl);

		ws.onmessage = (event) => {
			alert('Нове сповіщення: ' + event.data);
		};

		return () => {
			ws.close();
		};
	});

	function changeLanguage(lang: string) {
		$locale = lang;
		if (browser) {
			document.cookie = `locale=${lang}; path=/; max-age=${60 * 60 * 24 * 365}`;
		}
	}

	const createVisitMutation = createCreateVisitApiV1VisitsPost(undefined, () => queryClient);

	// Відстеження візитів при кожній зміні сторінки
	afterNavigate(({ to }) => {
		if (to) {
			createVisitMutation.mutate({
				data: {
					page_url: to.url.pathname,
					...(currentUserId ? { user_id: currentUserId } : {})
				}
			});
		}
	});

	function logout() {
		localStorage.removeItem('access_token');
		localStorage.removeItem('user_id');
		isLoggedIn = false;
		queryClient.clear();
		window.location.href = resolve('/');
	}
</script>

<QueryClientProvider client={queryClient}>
	{#if $isLoading}
		<div class="flex min-h-screen items-center justify-center bg-slate-50">
			<p class="text-lg font-medium text-slate-500">Завантаження...</p>
		</div>
	{:else}
		<div class="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900">
			<header
				class="sticky top-0 z-10 border-b border-slate-200 bg-white/80 shadow-sm backdrop-blur-md"
			>
				<div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
					<div class="flex-shrink-0">
						<a
							href={resolve('/')}
							class="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-2xl font-bold tracking-tight text-transparent"
							>RazomFund</a
						>
					</div>

					<nav class="hidden items-center space-x-6 md:flex">
						<div class="mr-2 flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1">
							<button
								class="text-sm font-bold transition-colors {$locale === 'uk'
									? 'text-blue-600'
									: 'text-slate-400 hover:text-slate-600'}"
								onclick={() => changeLanguage('uk')}
							>
								UK
							</button>
							<span class="text-slate-300">|</span>
							<button
								class="text-sm font-bold transition-colors {$locale === 'en'
									? 'text-blue-600'
									: 'text-slate-400 hover:text-slate-600'}"
								onclick={() => changeLanguage('en')}
							>
								EN
							</button>
						</div>

						<a
							href={resolve('/')}
							class="font-medium text-slate-600 transition-colors hover:text-blue-600"
						>
							{$_('nav.home')}
						</a>

						<a
							href={resolve('/campaigns')}
							class="font-medium text-slate-600 transition-colors hover:text-blue-600"
						>
							{$_('nav.campaigns')}
						</a>

						{#if isMounted}
							{#if isLoggedIn}
								<a
									href={resolve('/user-stats')}
									class="font-medium text-slate-600 transition-colors hover:text-blue-600"
								>
									{$_('nav.dashboard')}
								</a>

								<Button
									variant="ghost"
									class="ml-4 text-red-600 hover:bg-red-50 hover:text-red-700"
									onclick={logout}
								>
									{$_('nav.logout')}
								</Button>
							{:else}
								<div class="ml-4 flex items-center space-x-4 border-l border-slate-200 pl-4">
									<Button variant="ghost" href={resolve('/login')}>
										{$_('nav.login')}
									</Button>

									<Button
										href={resolve('/register')}
										class="bg-blue-600 shadow-sm hover:bg-blue-700"
									>
										{$_('nav.register')}
									</Button>
								</div>
							{/if}
						{/if}
					</nav>
				</div>
			</header>

			<main class="mx-auto w-full max-w-7xl flex-grow px-4 py-8 sm:px-6 lg:px-8">
				{@render children()}
			</main>

			<footer class="mt-auto border-t border-slate-200 bg-white">
				<div
					class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 py-6 sm:flex-row sm:px-6 lg:px-8"
				>
					<div class="text-sm text-slate-500">
						&copy; 2026 RazomFund Platform. {$_('footer.rights')}
					</div>
					<div
						class="flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm font-medium text-slate-600"
					>
						<a href={resolve('/')} class="transition-colors hover:text-blue-600"
							>{$_('footer.home')}</a
						>
						<a href={resolve('/campaigns')} class="transition-colors hover:text-blue-600"
							>{$_('footer.campaigns')}</a
						>
						<a href={resolve('/terms')} class="transition-colors hover:text-blue-600"
							>{$_('footer.terms')}</a
						>
						<a href={resolve('/faq')} class="transition-colors hover:text-blue-600"
							>{$_('footer.faq')}</a
						>
						<a href={resolve('/trust')} class="transition-colors hover:text-blue-600"
							>{$_('footer.trust')}</a
						>
						<a href={resolve('/contact')} class="transition-colors hover:text-blue-600"
							>{$_('footer.contact')}</a
						>
					</div>
				</div>
			</footer>
		</div>
	{/if}
</QueryClientProvider>
