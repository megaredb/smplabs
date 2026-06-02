<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
    import { ShieldCheck, UserCheck, AlertTriangle } from '@lucide/svelte';
</script>

<svelte:head>
    <title>{$_('trust.title')} | RazomFund</title>
</svelte:head>

<div class="mx-auto max-w-4xl py-12 px-4 sm:px-6">
    <div class="mb-10 text-center">
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">{$_('trust.title')}</h1>
        <p class="mt-4 text-lg text-slate-600">{$_('trust.intro')}</p>
    </div>

    <div class="grid gap-8 md:grid-cols-3">
        <Card class="border-none bg-blue-50/50 shadow-sm">
            <CardHeader class="text-center pb-2">
                <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                    <UserCheck class="h-6 w-6" />
                </div>
                <CardTitle class="text-xl">{$_('trust.verificationTitle')}</CardTitle>
            </CardHeader>
            <CardContent class="text-center text-slate-600">{$_('trust.verificationText')}</CardContent>
        </Card>

        <Card class="border-none bg-green-50/50 shadow-sm">
            <CardHeader class="text-center pb-2">
                <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
                    <ShieldCheck class="h-6 w-6" />
                </div>
                <CardTitle class="text-xl">{$_('trust.moderationTitle')}</CardTitle>
            </CardHeader>
            <CardContent class="text-center text-slate-600">{$_('trust.moderationText')}</CardContent>
        </Card>

        <Card class="border-none bg-orange-50/50 shadow-sm">
            <CardHeader class="text-center pb-2">
                <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-orange-100 text-orange-600">
                    <AlertTriangle class="h-6 w-6" />
                </div>
                <CardTitle class="text-xl">{$_('trust.reportingTitle')}</CardTitle>
            </CardHeader>
            <CardContent class="text-center text-slate-600">{$_('trust.reportingText')}</CardContent>
        </Card>
    </div>
</div>