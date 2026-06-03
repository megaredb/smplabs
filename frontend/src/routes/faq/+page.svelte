<script lang="ts">
	import { _ } from 'svelte-i18n';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { HelpCircle } from '@lucide/svelte';
</script>

<svelte:head>
	<title>{$_('faq.title')} | RazomFund</title>
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-12 sm:px-6">
	<div class="mb-10 text-center">
		<div
			class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-blue-600"
		>
			<HelpCircle class="h-8 w-8" />
		</div>
		<h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">{$_('faq.title')}</h1>
	</div>

	<div class="space-y-6">
		<Card class="border-slate-200 shadow-sm">
			<CardHeader><CardTitle class="text-lg">{$_('faq.q1')}</CardTitle></CardHeader>
			<CardContent class="leading-relaxed text-slate-600">{$_('faq.a1')}</CardContent>
		</Card>

		<Card class="border-slate-200 shadow-sm">
			<CardHeader><CardTitle class="text-lg">{$_('faq.q2')}</CardTitle></CardHeader>
			<CardContent class="leading-relaxed text-slate-600">{$_('faq.a2')}</CardContent>
		</Card>

		<Card class="border-slate-200 shadow-sm">
			<CardHeader><CardTitle class="text-lg">{$_('faq.q3')}</CardTitle></CardHeader>
			<CardContent class="leading-relaxed text-slate-600">{$_('faq.a3')}</CardContent>
		</Card>
	</div>
</div>
