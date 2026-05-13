<script lang="ts">
    import { goto } from '$app/navigation';

    let title = $state('');
    let description = $state('');
    let targetAmount = $state('');
    
    let isLoading = $state(false);
    let errorMessage = $state('');

    let isSuccess = $state(false);

    async function handleSubmit(event: Event) {
        event.preventDefault(); 
        isLoading = true;
        errorMessage = '';

        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                throw new Error('Ви не авторизовані!');
            }

            const tokenPayload = JSON.parse(atob(token.split('.')[1]));
            
            const currentUserId = parseInt(tokenPayload.sub);

            const response = await fetch('http://127.0.0.1:8000/api/v1/campaigns/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` 
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    target_amount: parseFloat(targetAmount),
                    organizer_id: currentUserId 
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (Array.isArray(errorData.detail)) {
                    const messages = errorData.detail.map((err: any) => `${err.loc.join('.')}: ${err.msg}`);
                    throw new Error(messages.join(' | '));
                }
                throw new Error(typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData));
            }

            isSuccess = true;
            
            setTimeout(() => {
                goto('/campaigns');
            }, 2000);

        } catch (error: any) {
            errorMessage = error.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-2xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-8 mt-6">
    <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">Створити новий збір</h1>
        <p class="text-gray-500 mt-1">Заповніть деталі, щоб розпочати залучення коштів.</p>
    </div>

    {#if errorMessage}
        <div class="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {errorMessage}
        </div>
    {/if}
    
    {#if isSuccess}
        <div class="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg flex items-center animate-bounce">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Збір успішно створено! Зараз ви будете перенаправлені...
        </div>
    {/if}

    <form onsubmit={handleSubmit} class="space-y-6">
        <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Назва збору</label>
            <input 
                id="title" 
                type="text" 
                bind:value={title} 
                required 
                placeholder="Наприклад: Збір на дрони для 3 ОШБр"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            />
        </div>

        <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Опис (мета збору)</label>
            <textarea 
                id="description" 
                bind:value={description} 
                required 
                rows="4" 
                placeholder="Розкажіть детальніше, на що саме збираються кошти..."
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all resize-y"
            ></textarea>
        </div>

        <div>
            <label for="amount" class="block text-sm font-medium text-gray-700 mb-1">Цільова сума (грн)</label>
            <input 
                id="amount" 
                type="number" 
                bind:value={targetAmount} 
                required 
                min="1" 
                placeholder="50000"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            />
        </div>

        <div class="flex justify-end space-x-4 pt-4 border-t border-gray-100">
            <a 
                href="/campaigns" 
                class="px-5 py-2 text-gray-700 font-medium hover:bg-gray-100 rounded-lg transition-colors"
            >
                Скасувати
            </a>
            <button 
                type="submit" 
                disabled={isLoading}
                class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2 rounded-lg font-medium transition-colors shadow-sm flex items-center"
            >
                {#if isLoading}
                    <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Створення...
                {:else}
                    Створити збір
                {/if}
            </button>
        </div>
    </form>
</div>