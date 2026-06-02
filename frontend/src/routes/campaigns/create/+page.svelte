<script lang="ts">
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';
  import { createCreateCampaignApiV1CampaignsPost } from '$lib/api/generated/endpoints';
  import { onMount } from 'svelte';
  import { _ } from 'svelte-i18n';

  let title = $state('');
  let description = $state('');
  let targetAmount = $state('');
  let endDate = $state('');
  let imageUrl = $state('');
  let category = $state('Інше'); // НОВЕ: категорія за замовчуванням

  let errorMessage = $state('');
  let isSuccess = $state(false);
  let currentUserId = $state<number | null>(null);

  const createMutation = createCreateCampaignApiV1CampaignsPost();

  const categoryOptions = [
    { id: "ЗСУ / Військові", key: 'categories.military' },
    { id: "Медицина", key: 'categories.medical' },
    { id: "Відбудова", key: 'categories.rebuild' },
    { id: "Тварини", key: 'categories.animals' },
    { id: "Інше", key: 'categories.other' }
    ];

  onMount(() => {
      const token = localStorage.getItem('access_token');
      if (token) {
          try {
              const tokenPayload = JSON.parse(atob(token.split('.')[1]));
              currentUserId = parseInt(tokenPayload.sub);
          } catch {}
      }
  });

  function handleSubmit(event: Event) {
      event.preventDefault();
      errorMessage = '';

      if (!currentUserId) {
          errorMessage = $_('createCampaign.authError');
          return;
      }

      createMutation.mutate(
          {
              data: {
                  title: title,
                  description: description,
                  target_amount: parseFloat(targetAmount),
                  organizer_id: currentUserId,
                  end_date: endDate ? new Date(endDate).toISOString() : undefined,
                  image_url: imageUrl || undefined,
                  category: category // НОВЕ: передаємо категорію
              } as any
          },
          {
              onSuccess: () => {
                  isSuccess = true;
                  setTimeout(() => {
                      goto(resolve('/campaigns'));
                  }, 2000);
              },
              onError: (error: unknown) => {
                  const err = error as { response?: { data?: { detail?: any } } };
                  const detail = err.response?.data?.detail;
                  // НОВЕ: Правильна обробка Validation Error від FastAPI
                  errorMessage = Array.isArray(detail) 
                      ? detail.map(d => d.msg).join(', ') 
                      : detail || $_('createCampaign.defaultError');
              }
          }
      );
  }
</script>

<div class="mx-auto mt-6 max-w-2xl rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
  <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">{$_('createCampaign.heading')}</h1>
      <p class="mt-1 text-gray-500">{$_('createCampaign.subheading')}</p>
  </div>

  {#if errorMessage}
      <div class="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
          {errorMessage}
      </div>
  {/if}

  {#if isSuccess}
      <div class="mb-6 flex items-center rounded-lg border border-green-200 bg-green-50 p-4 text-green-700">
          {$_('createCampaign.successMessage')}
      </div>
  {/if}

  <form onsubmit={handleSubmit} class="space-y-6">
      <div>
          <label for="title" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.titleLabel')}</label>
          <input id="title" type="text" bind:value={title} required placeholder={$_('createCampaign.titlePlaceholder')} class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500" />
      </div>

      <div>
          <label for="description" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.descLabel')}</label>
          <textarea id="description" bind:value={description} required rows="4" placeholder={$_('createCampaign.descPlaceholder')} class="w-full resize-y rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"></textarea>
      </div>

      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
              <label for="amount" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.targetLabel')}</label>
              <input id="amount" type="number" bind:value={targetAmount} required min="1" placeholder="50000" class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
                <label for="category" class="mb-1 block text-sm font-medium text-gray-700">{$_('categories.label')}</label>
                <select id="category" bind:value={category} class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500">
                    {#each categoryOptions as cat}
                        <option value={cat.id}>{$_(cat.key)}</option>
                    {/each}
                </select>
            </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
              <label for="endDate" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.endDateLabel')}</label>
              <input id="endDate" type="date" bind:value={endDate} class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
              <label for="imageUrl" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.imageUrlLabel')}</label>
              <input id="imageUrl" type="url" bind:value={imageUrl} placeholder={$_('createCampaign.imageUrlPlaceholder')} class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500" />
          </div>
      </div>

      <div class="flex justify-end space-x-4 border-t border-gray-100 pt-4">
          <a href={resolve('/campaigns')} class="rounded-lg px-5 py-2 font-medium text-gray-700 transition-colors hover:bg-gray-100">
              {$_('createCampaign.cancelBtn')}
          </a>
          <button type="submit" disabled={createMutation.isPending} class="flex items-center rounded-lg bg-blue-600 px-6 py-2 font-medium text-white shadow-sm transition-colors hover:bg-blue-700 disabled:bg-blue-400">
              {#if createMutation.isPending}
                  {$_('createCampaign.creatingBtn')}
              {:else}
                  {$_('createCampaign.submitBtn')}
              {/if}
          </button>
      </div>
  </form>
</div>