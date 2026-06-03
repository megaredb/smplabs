<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { ArrowRight, Heart, ShieldCheck, Zap } from '@lucide/svelte';
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';

	// ДОДАНО: імпорт функції перекладу
	import { _ } from 'svelte-i18n';

	let currentUserId = $state<number | null>(null);

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
	<title>{$_('home.pageTitle')}</title>
</svelte:head>

<div class="flex min-h-[70vh] flex-col items-center justify-center space-y-12 text-center">
	<div class="max-w-3xl space-y-6">
		<h1 class="text-5xl leading-tight font-extrabold tracking-tight text-slate-900 sm:text-6xl">
			{$_('home.heroTitle1')} <br />
			<span class="bg-linear-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
				{$_('home.heroTitle2')}
			</span>
		</h1>
		<p class="mx-auto max-w-2xl text-xl leading-relaxed text-slate-600">
			{$_('home.heroDesc')}
		</p>

		<div class="flex flex-col items-center justify-center gap-4 pt-4 sm:flex-row">
			<Button
				size="lg"
				href={resolve('/campaigns')}
				class="w-full gap-2 rounded-full bg-blue-600 px-8 py-6 text-lg shadow-lg transition-all hover:bg-blue-700 hover:shadow-xl sm:w-auto"
			>
				{$_('home.viewCampaigns')}
				<ArrowRight class="h-5 w-5" />
			</Button>
			{#if currentUserId}
				<Button
					size="lg"
					variant="outline"
					href={resolve('/campaigns/create')}
					class="w-full rounded-full border-slate-300 px-8 py-6 text-lg sm:w-auto"
				>
					{$_('home.createCampaign')}
				</Button>
			{/if}
		</div>
	</div>

	<div
		class="mt-12 grid w-full max-w-5xl grid-cols-1 gap-8 border-t border-slate-200/60 pt-12 md:grid-cols-3"
	>
		<div class="flex flex-col items-center space-y-3 p-6 text-center">
			<div class="mb-2 rounded-2xl bg-blue-100 p-4 text-blue-600">
				<ShieldCheck class="h-8 w-8" />
			</div>
			<h3 class="text-xl font-bold text-slate-900">{$_('home.features.transparencyTitle')}</h3>
			<p class="text-slate-600">{$_('home.features.transparencyDesc')}</p>
		</div>

		<div class="flex flex-col items-center space-y-3 p-6 text-center">
			<div class="mb-2 rounded-2xl bg-indigo-100 p-4 text-indigo-600">
				<Zap class="h-8 w-8" />
			</div>
			<h3 class="text-xl font-bold text-slate-900">{$_('home.features.speedTitle')}</h3>
			<p class="text-slate-600">{$_('home.features.speedDesc')}</p>
		</div>

		<div class="flex flex-col items-center space-y-3 p-6 text-center">
			<div class="mb-2 rounded-2xl bg-rose-100 p-4 text-rose-600">
				<Heart class="h-8 w-8" />
			</div>
			<h3 class="text-xl font-bold text-slate-900">{$_('home.features.trustTitle')}</h3>
			<p class="text-slate-600">{$_('home.features.trustDesc')}</p>
		</div>
	</div>
</div>
