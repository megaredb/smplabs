<script lang="ts">
	import { _ } from 'svelte-i18n';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { ShieldCheck, CreditCard, Users } from '@lucide/svelte';
</script>

<svelte:head>
	<title>{$_('terms.title')} | RazomFund</title>
</svelte:head>

<div class="mx-auto max-w-4xl py-8">
	<div class="mb-10 text-center">
		<h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
			{$_('terms.title')}
		</h1>
		<div class="mx-auto mt-4 h-1 w-20 rounded bg-blue-600"></div>
	</div>

	<div class="space-y-8">
		<Card class="border-none shadow-md">
			<CardHeader class="flex flex-row items-center gap-4 pb-2">
				<div
					class="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600"
				>
					<Users class="h-6 w-6" />
				</div>
				<CardTitle class="text-2xl">{$_('terms.aboutTitle')}</CardTitle>
			</CardHeader>
			<CardContent>
				<p class="text-lg leading-relaxed text-slate-600">
					{$_('terms.aboutText')}
				</p>
			</CardContent>
		</Card>

		<Card class="border-none shadow-md">
			<CardHeader class="flex flex-row items-center gap-4 pb-2">
				<div
					class="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600"
				>
					<CreditCard class="h-6 w-6" />
				</div>
				<CardTitle class="text-2xl">{$_('terms.commissionTitle')}</CardTitle>
			</CardHeader>
			<CardContent>
				<p class="text-lg leading-relaxed text-slate-600">
					{$_('terms.commissionText')}
				</p>
			</CardContent>
		</Card>

		<Card class="border-none shadow-md">
			<CardHeader class="flex flex-row items-center gap-4 pb-2">
				<div
					class="flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600"
				>
					<ShieldCheck class="h-6 w-6" />
				</div>
				<CardTitle class="text-2xl">{$_('terms.rulesTitle')}</CardTitle>
			</CardHeader>
			<CardContent>
				<p class="text-lg leading-relaxed text-slate-600">
					{$_('terms.rulesText')}
				</p>
			</CardContent>
		</Card>
	</div>
</div>
