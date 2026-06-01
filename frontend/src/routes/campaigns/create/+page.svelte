<script lang="ts">
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';
  import { createCreateCampaignApiV1CampaignsPost } from '$lib/api/generated/endpoints';
  import { onMount } from 'svelte';
  
  // ДОДАНО: імпорт перекладу
  import { _ } from 'svelte-i18n';

  let title = $state('');
  let description = $state('');
  let targetAmount = $state('');
  let errorMessage = $state('');
  let isSuccess = $state(false);
  let currentUserId = $state<number | null>(null);

  const createMutation = createCreateCampaignApiV1CampaignsPost();

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
          organizer_id: currentUserId
        }
      },
      {
        onSuccess: () => {
          isSuccess = true;
          setTimeout(() => {
            goto(resolve('/campaigns'));
          }, 2000);
        },
        onError: (error: unknown) => {
          const err = error as { response?: { data?: { detail?: string } } };
          errorMessage = err.response?.data?.detail || $_('createCampaign.defaultError');
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
      <svg xmlns="http://www.w3.org/2000/svg" class="mr-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      {$_('createCampaign.successMessage')}
    </div>
  {/if}

  <form onsubmit={handleSubmit} class="space-y-6">
    <div>
      <label for="title" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.titleLabel')}</label>
      <input
        id="title"
        type="text"
        bind:value={title}
        required
        placeholder={$_('createCampaign.titlePlaceholder')}
        class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label for="description" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.descLabel')}</label>
      <textarea
        id="description"
        bind:value={description}
        required
        rows="4"
        placeholder={$_('createCampaign.descPlaceholder')}
        class="w-full resize-y rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
      ></textarea>
    </div>

    <div>
      <label for="amount" class="mb-1 block text-sm font-medium text-gray-700">{$_('createCampaign.targetLabel')}</label>
      <input
        id="amount"
        type="number"
        bind:value={targetAmount}
        required
        min="1"
        placeholder="50000"
        class="w-full rounded-lg border border-gray-300 px-4 py-2 transition-all outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div class="flex justify-end space-x-4 border-t border-gray-100 pt-4">
      <a href={resolve('/campaigns')} class="rounded-lg px-5 py-2 font-medium text-gray-700 transition-colors hover:bg-gray-100">
        {$_('createCampaign.cancelBtn')}
      </a>
      <button
        type="submit"
        disabled={createMutation.isPending}
        class="flex items-center rounded-lg bg-blue-600 px-6 py-2 font-medium text-white shadow-sm transition-colors hover:bg-blue-700 disabled:bg-blue-400"
      >
        {#if createMutation.isPending}
          <svg class="mr-2 -ml-1 h-5 w-5 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {$_('createCampaign.creatingBtn')}
        {:else}
          {$_('createCampaign.submitBtn')}
        {/if}
      </button>
    </div>
  </form>
</div>