<script lang="ts">
	import './app.css';
	import { onMount } from 'svelte';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import { browser } from '$app/environment';
	import { Button } from '$lib/components/ui/button';
	import { resolve } from '$app/paths';

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

	onMount(() => {
		if (localStorage.getItem('access_token')) {
			isLoggedIn = true;
			// Optionally fetch user info here
		}
	});

	function logout() {
		localStorage.removeItem('access_token');
		isLoggedIn = false;
		queryClient.clear();
		window.location.href = resolve('/');
	}
</script>

<QueryClientProvider client={queryClient}>
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
					<a
						href={resolve('/')}
						class="font-medium text-slate-600 transition-colors hover:text-blue-600">Головна</a
					>
					<a
						href={resolve('/campaigns')}
						class="font-medium text-slate-600 transition-colors hover:text-blue-600">Збори</a
					>
					{#if isLoggedIn}
						<a
							href={resolve('/user-stats')}
							class="font-medium text-slate-600 transition-colors hover:text-blue-600"
							>Мій кабінет</a
						>
					{/if}

					{#if isLoggedIn}
						<Button
							variant="ghost"
							class="ml-4 text-red-600 hover:bg-red-50 hover:text-red-700"
							onclick={logout}>Вийти</Button
						>
					{:else}
						<div class="ml-4 flex items-center space-x-4 border-l border-slate-200 pl-4">
							<Button variant="ghost" href={resolve('/login')}>Увійти</Button>
							<Button href={resolve('/register')} class="bg-blue-600 shadow-sm hover:bg-blue-700"
								>Реєстрація</Button
							>
						</div>
					{/if}
				</nav>
			</div>
		</header>

		<main class="mx-auto w-full max-w-7xl flex-grow px-4 py-8 sm:px-6 lg:px-8">
			{@render children()}
		</main>

		<footer class="mt-auto border-t border-slate-200 bg-white">
			<div class="mx-auto max-w-7xl px-4 py-6 text-center text-sm text-slate-500 sm:px-6 lg:px-8">
				&copy; 2026 RazomFund Platform. Усі права захищено.
			</div>
		</footer>
	</div>
</QueryClientProvider>
