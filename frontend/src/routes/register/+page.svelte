<script lang="ts">
    import { goto } from '$app/navigation';

    let email = $state('');
    let name = $state('');
    let password = $state('');
    
    let isLoading = $state(false);
    let errorMessage = $state('');

    async function handleRegister(event: Event) {
        event.preventDefault();
        isLoading = true;
        errorMessage = '';

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email, 
                    password,
                    name, 
                    role: "donor",
                    is_active: true,
                    is_superuser: false,
                    is_verified: false
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Помилка реєстрації');
            }

            await goto('/login');
        } catch (error: any) {
            errorMessage = error.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-md mx-auto mt-16 bg-white p-8 rounded-xl shadow-sm border border-gray-200">
    <h1 class="text-2xl font-bold text-center text-gray-900 mb-6">Створення акаунта</h1>

    {#if errorMessage}
        <div class="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">{errorMessage}</div>
    {/if}

    <form onsubmit={handleRegister} class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" bind:value={email} required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input type="password" bind:value={password} required minlength="8" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ім'я</label>
            <input type="text" bind:value={name} required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        <button type="submit" disabled={isLoading} class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium mt-4">
            {isLoading ? 'Реєстрація...' : 'Зареєструватися'}
        </button>
    </form>
    
    <p class="text-center mt-4 text-sm text-gray-600">
        Вже маєте акаунт? <a href="/login" class="text-blue-600 hover:underline">Увійти</a>
    </p>
</div>