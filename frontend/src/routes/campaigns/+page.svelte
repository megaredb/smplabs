<script lang="ts">
  import {
    createGetTopCampaignsApiV1CampaignsTopGet,
    createDeleteCampaignApiV1CampaignsCampaignIdDelete
  } from '$lib/api/generated/endpoints';
  import type { CampaignResponse } from '$lib/api/generated/model';
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Progress } from '$lib/components/ui/progress';
  import { Input } from '$lib/components/ui/input';
  import { Plus, Search, Trash2, Clock, Calendar, Filter, ArrowUpDown } from '@lucide/svelte';
  import { onMount } from 'svelte';
  import { resolve } from '$app/paths';
  
  // ДОДАНО: імпорт перекладу
  import { _ } from 'svelte-i18n';

  let selectedCategory = $state<string | undefined>(undefined);
  let sortBy = $state('current_amount'); // НОВЕ: сортування
  let searchQuery = $state('');
  let currentUserId = $state<number | null>(null);

  const categoryOptions = [
        { id: "ЗСУ / Військові", key: 'categories.military' },
        { id: "Медицина", key: 'categories.medical' },
        { id: "Відбудова", key: 'categories.rebuild' },
        { id: "Тварини", key: 'categories.animals' },
        { id: "Інше", key: 'categories.other' }
    ];

    function translateCategory(cat: string) {
        const match = categoryOptions.find(c => c.id === cat);
        return match ? $_(match.key) : (cat || $_('categories.other'));
    }

  const campaignsQuery = $derived(
      createGetTopCampaignsApiV1CampaignsTopGet(() => ({
          limit: 50,
          category: selectedCategory === "all" ? undefined : selectedCategory,
          sort_by: sortBy
      } as any)) // as any потрібен, поки типи orval не оновлено
  );
  const deleteMutation = createDeleteCampaignApiV1CampaignsCampaignIdDelete();

  onMount(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        currentUserId = parseInt(payload.sub);
      } catch {}
    }
  });

  function getCampaigns(): CampaignResponse[] {
    const d = campaignsQuery.data;
    if (!d) return [];
    if (Array.isArray(d)) return d as CampaignResponse[];
    if (typeof d === 'object' && d !== null && 'data' in d) {
      const safeData = (d as Record<string, unknown>).data;
      if (Array.isArray(safeData)) {
        return safeData as CampaignResponse[];
      }
    }
    return [];
  }

  let filterLimit = $state(50);
  let filteredCampaigns = $derived(
    getCampaigns()
      .slice(0, filterLimit)
      .filter(
        (c) =>
          c.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          c.description?.toLowerCase().includes(searchQuery.toLowerCase())
      )
  );

  function handleDelete(id: number) {
    if (!confirm($_('campaigns.deleteConfirm'))) return;
    deleteMutation.mutate(
      { campaignId: id },
      {
        onSuccess: () => campaignsQuery.refetch(),
        onError: () => alert($_('campaigns.deleteError'))
      }
    );
  }

</script>

<svelte:head>
  <title>{$_('campaigns.pageTitle')}</title>
</svelte:head>

<div class="mx-auto max-w-6xl space-y-8">
  <div class="flex flex-col items-start justify-between gap-4 rounded-2xl border border-slate-200/60 bg-white/60 p-6 shadow-sm backdrop-blur-sm sm:flex-row sm:items-center">
    <h1 class="text-3xl font-bold tracking-tight text-slate-900">{$_('campaigns.heading')}</h1>
    <div class="flex w-full flex-col items-center gap-4 sm:w-auto sm:flex-row">
      <div class="relative w-full sm:w-48">
          <Filter class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <select
                bind:value={selectedCategory}
                class="flex h-10 w-full cursor-pointer appearance-none items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2 pl-9 text-sm ring-offset-white transition-all focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
                <option value="all">{$_('categories.all')}</option>
                {#each categoryOptions as cat}
                    <option value={cat.id}>{$_(cat.key)}</option>
                {/each}
            </select>
      </div>
      <div class="relative w-full sm:w-48">
          <ArrowUpDown class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <div class="relative w-full sm:w-48">
                        <ArrowUpDown class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400" />
                        <select
                            bind:value={sortBy}
                            class="flex h-10 w-full cursor-pointer appearance-none items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2 pl-9 text-sm ring-offset-white transition-all focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        >
                            <option value="current_amount">{$_('sorting.amount')}</option>
                            <option value="target">{$_('sorting.target')}</option>
                            <option value="date">{$_('sorting.newest')}</option>
                        </select>
                    </div>
      </div>
      <div class="relative w-full sm:w-72">
        <Search class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <Input
          type="text"
          bind:value={searchQuery}
          placeholder={$_('campaigns.searchPlaceholder')}
          class="bg-white pl-9"
        />
      </div>
      <Button
        href={resolve('/campaigns/create')}
        class="w-full gap-2 bg-blue-600 hover:bg-blue-700 sm:w-auto"
      >
        <Plus class="h-4 w-4" />
        {$_('campaigns.createBtn')}
      </Button>
    </div>
  </div>

  {#if campaignsQuery.isLoading}
    <div class="flex items-center justify-center py-20">
      <div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
    </div>
  {:else if campaignsQuery.isError}
    <Card class="border-red-200 bg-red-50/50">
      <CardContent class="py-10 text-center text-red-600">
        <p class="font-medium">{$_('campaigns.loadError')}</p>
        <Button variant="outline" class="mt-4" onclick={() => campaignsQuery.refetch()}>
          {$_('campaigns.retryBtn')}
        </Button>
      </CardContent>
    </Card>
  {:else}
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      {#each filteredCampaigns as campaign (campaign.id)}
        <Card class="group relative flex h-full flex-col overflow-hidden border-slate-200/60 bg-white/80 backdrop-blur-sm transition-all hover:shadow-lg">
          {#if currentUserId === campaign.organizer_id}
            <Button
              variant="destructive"
              size="icon"
              class="absolute top-3 right-3 z-10 h-8 w-8 rounded-full opacity-0 shadow-md transition-opacity group-hover:opacity-100"
              onclick={() => handleDelete(campaign.id)}
              title={$_('campaigns.deleteBtnTitle')}
            >
              <Trash2 class="h-4 w-4" />
            </Button>
          {/if}
          <a href={resolve(`/campaigns/${campaign.id}`)} class="flex flex-1 flex-col hover:no-underline">
                        {#if (campaign as any).image_url}
                            <img src={(campaign as any).image_url} alt={campaign.title} class="h-48 w-full object-cover" />
                        {:else}
                            <div class="flex h-48 w-full items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
                                <span class="font-medium text-slate-400">{$_('campaigns.noPhoto')}</span>
                            </div>
                        {/if}
                        
                        <CardHeader class="flex-none">
                            <div class="mb-2">
                                <span class="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                                    {translateCategory((campaign as any).category)}
                                </span>
                            </div>
                            <CardTitle class="line-clamp-2 leading-tight transition-colors group-hover:text-blue-600">{campaign.title}</CardTitle>
                        </CardHeader>
                        <CardContent class="flex grow flex-col">
                            <CardDescription class="mb-4 line-clamp-3 text-slate-600">{campaign.description}</CardDescription>
                            <div class="mb-5 flex flex-col gap-1.5 text-xs">
                                <div class="flex items-center gap-1.5 text-slate-500">
                                    <Clock class="h-3.5 w-3.5" />
                                    <span>{$_('campaigns.createdAt')} {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString('uk-UA') : '—'}</span>
                                </div>
                                <div class="flex items-center gap-1.5 font-medium text-blue-600/80">
                                    <Calendar class="h-3.5 w-3.5" />
                                    <span>{$_('campaigns.endingAt')} {(campaign as any).end_date ? new Date((campaign as any).end_date).toLocaleDateString('uk-UA') : '—'}</span>
                                </div>
                            </div>
                            <div class="mt-auto space-y-3">
                <div class="flex items-end justify-between text-sm">
                  <div class="flex flex-col">
                    <span class="text-xs text-slate-500">{$_('campaigns.collected')}</span>
                    <span class="text-lg leading-none font-bold text-slate-900">{campaign.current_amount ?? 0} ₴</span>
                  </div>
                  <div class="flex flex-col items-end">
                    <span class="text-xs text-slate-500">{$_('campaigns.target')}</span>
                    <span class="font-medium text-slate-600">{campaign.target_amount} ₴</span>
                  </div>
                </div>
                <Progress
                  value={Math.min(((campaign.current_amount ?? 0) / (Number(campaign.target_amount) || 1)) * 100, 100)}
                  class="h-2 bg-slate-100 [&>div]:bg-blue-600"
                />
              </div>
            </CardContent>
          </a>
        </Card>
      {:else}
        <div class="col-span-full flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-200 bg-white/50 py-20 text-center backdrop-blur-sm">
          <div class="mb-4 rounded-full bg-slate-100 p-4">
            <Search class="h-8 w-8 text-slate-400" />
          </div>
          <h3 class="mb-2 text-xl font-semibold text-slate-900">{$_('campaigns.notFoundTitle')}</h3>
          <p class="max-w-sm text-slate-500">{$_('campaigns.notFoundDesc')}</p>
        </div>
      {/each}
    </div>
  {/if}
</div>