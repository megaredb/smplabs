<script lang="ts">
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Search, BarChart2, Globe, User } from '@lucide/svelte';

	import { createGetVisitStatsApiV1VisitsStatsGet } from '$lib/api/generated/endpoints';
	import type { VisitStatsResponse } from '$lib/api/generated/model';

	let inputUrl = $state('/'); // Temporary value before search
	let targetUrl = $state('/'); // Value used for query
	let currentUserId = $state<number | null>(null);

	const statsQuery = $derived(
		createGetVisitStatsApiV1VisitsStatsGet(
			() => ({
				page_url: targetUrl,
				...(currentUserId ? { user_id: currentUserId } : {})
			}),
			() => ({ query: { enabled: !!targetUrl, retry: false } })
		)
	);

	let isLoading = $derived(statsQuery.isFetching);
	let error = $derived(statsQuery.isError ? 'Не вдалося завантажити статистику. Перевірте правильність URL.' : '');
	let stats = $derived(statsQuery.data as unknown as VisitStatsResponse | undefined);

	function fetchStats() {
		targetUrl = inputUrl;
	}

	onMount(() => {
		const token = localStorage.getItem('access_token');
		if (token) {
			try {
				const payload = JSON.parse(atob(token.split('.')[1]));
				currentUserId = parseInt(payload.sub);
			} catch {}
		}
	});
</script>

<svelte:head>
	<title>RazomFund - Аналітика відвідувань</title>
</svelte:head>

<div class="mx-auto max-w-6xl space-y-8">
	<div
		class="flex flex-col items-start justify-between gap-4 rounded-2xl border border-slate-200/60 bg-white/60 p-6 shadow-sm backdrop-blur-sm sm:flex-row sm:items-center"
	>
		<h1 class="text-3xl font-bold tracking-tight text-slate-900">Аналітика відвідувань</h1>

		<div class="flex w-full flex-col items-center gap-4 sm:w-auto sm:flex-row">
			<div class="relative w-full sm:w-72">
				<Search class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400" />
				<Input
					type="text"
					bind:value={inputUrl}
					placeholder="Введіть URL (наприклад, /campaigns/1)"
					class="bg-white pl-9"
					onkeydown={(e) => e.key === 'Enter' && fetchStats()}
				/>
			</div>

			<Button
				onclick={fetchStats}
				disabled={isLoading}
				class="w-full gap-2 bg-blue-600 hover:bg-blue-700 sm:w-auto"
			>
				<BarChart2 class="h-4 w-4" />
				Перевірити
			</Button>
		</div>
	</div>

	{#if isLoading}
		<div class="flex items-center justify-center py-20">
			<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
		</div>
	{:else if error}
		<Card class="border-red-200 bg-red-50/50">
			<CardContent class="py-10 text-center text-red-600">
				<p class="font-medium">{error}</p>
				<Button variant="outline" class="mt-4" onclick={fetchStats}>Спробувати знову</Button>
			</CardContent>
		</Card>
	{:else if stats}
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
			<Card
				class="group relative flex h-full flex-col overflow-hidden border-slate-200/60 bg-white/80 backdrop-blur-sm transition-all hover:shadow-lg"
			>
				<CardHeader class="flex-none border-b border-slate-100 bg-slate-50/50 pb-4">
					<div class="flex items-center gap-2">
						<div class="rounded-full bg-blue-100 p-2 text-blue-600">
							<Globe class="h-5 w-5" />
						</div>
						<CardTitle class="text-lg font-semibold text-slate-700">Загалом переглядів</CardTitle>
					</div>
				</CardHeader>

				<CardContent class="flex grow flex-col items-center justify-center py-12">
					<span class="text-7xl font-bold tracking-tight text-slate-900">{stats.total_visits}</span>
					<div class="mt-4 rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-500">
						сторінка <span class="font-mono text-blue-600">{stats.page_url}</span>
					</div>
				</CardContent>
			</Card>

			<Card
				class="group relative flex h-full flex-col overflow-hidden border-slate-200/60 bg-white/80 backdrop-blur-sm transition-all hover:shadow-lg"
			>
				<CardHeader class="flex-none border-b border-slate-100 bg-slate-50/50 pb-4">
					<div class="flex items-center gap-2">
						<div class="rounded-full bg-indigo-100 p-2 text-indigo-600">
							<User class="h-5 w-5" />
						</div>
						<CardTitle class="text-lg font-semibold text-slate-700">Ваші перегляди</CardTitle>
					</div>
				</CardHeader>

				<CardContent class="flex grow flex-col items-center justify-center py-12">
					<span class="text-7xl font-bold tracking-tight text-slate-900">{stats.user_visits}</span>
					<div class="mt-4 rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-500">
						авторизований трафік
					</div>
				</CardContent>
			</Card>
		</div>
	{/if}
</div>
