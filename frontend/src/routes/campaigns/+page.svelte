<script lang="ts">
    import type { PageData } from './$types';
    import { onMount } from 'svelte';

    let { data }: { data: PageData } = $props();

    let campaigns = $state(data.campaigns);
    
    let searchQuery = $state('');
    let currentUserId = $state<number | null>(null);

    onMount(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const tokenPayload = JSON.parse(atob(token.split('.')[1]));
                currentUserId = parseInt(tokenPayload.sub);
            } catch (e) {
                console.error("Помилка читання токена");
            }
        }
    });

    let filteredCampaigns = $derived(
        campaigns.filter((campaign: any) => 
            campaign.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
            campaign.description.toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    async function handleDelete(id: number) {
        if (!confirm('Ви впевнені, що хочете видалити цей збір? Цю дію неможливо скасувати.')) {
            return;
        }

        const token = localStorage.getItem('access_token');

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/campaigns/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Не вдалося видалити збір на сервері');
            }

            campaigns = campaigns.filter((c: any) => c.id !== id);
            
        } catch (error) {
            console.error(error);
            alert('Помилка при видаленні збору. Перевірте консоль.');
        }
    }
</script>

<div class="space-y-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
        <h1 class="text-2xl font-bold text-gray-900">Усі збори</h1>
        
        <div class="flex flex-col sm:flex-row w-full sm:w-auto gap-3">
            <div class="relative w-full sm:w-64">
                <input 
                    type="text" 
                    bind:value={searchQuery}
                    placeholder="Знайти збір..." 
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                />
            </div>
            
            <a href="/campaigns/create" class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg font-medium transition-colors shadow-sm flex items-center justify-center whitespace-nowrap">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                </svg>
                Створити збір
            </a>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each filteredCampaigns as campaign}
            <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-all flex flex-col h-full group relative">
                
                {#if currentUserId === campaign.organizer_id}
                    <button 
                        onclick={() => handleDelete(campaign.id)}
                        class="absolute top-4 right-4 text-gray-400 hover:text-red-500 transition-colors bg-white rounded-full p-1 shadow-sm border border-gray-100 opacity-0 group-hover:opacity-100"
                        title="Видалити збір"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                {/if}

                <h2 class="text-xl font-semibold text-gray-800 mb-2 group-hover:text-blue-600 transition-colors pr-6">{campaign.title}</h2>
                <p class="text-gray-600 mb-6 flex-grow line-clamp-3 leading-relaxed">{campaign.description}</p>
                
                <div class="space-y-3 mt-auto">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Зібрано: <span class="font-bold text-gray-900">{campaign.current_amount} ₴</span></span>
                        <span class="text-gray-500">Ціль: <span class="font-bold text-gray-900">{campaign.target_amount} ₴</span></span>
                    </div>
                    
                    <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                        <div 
                            class="bg-blue-600 h-2.5 rounded-full transition-all duration-500" 
                            style="width: {Math.min((campaign.current_amount / campaign.target_amount) * 100, 100)}%">
                        </div>
                    </div>
                </div>
            </div>
        {:else}
            <div class="col-span-full text-center py-16 bg-white rounded-xl border border-gray-200 border-dashed">
                <h3 class="text-lg font-medium text-gray-900">Зборів не знайдено</h3>
                <p class="text-gray-500 mt-1">Спробуйте змінити пошуковий запит або створіть перший збір.</p>
            </div>
        {/each}
    </div>
</div>