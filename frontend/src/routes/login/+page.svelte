<script lang="ts">
    import { goto } from '$app/navigation';

    let email = $state('');
    let password = $state('');
    
    let isLoading = $state(false);
    let errorMessage = $state('');

    async function handleLogin(event: Event) {
        event.preventDefault();
        isLoading = true;
        errorMessage = '';

        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch('http://127.0.0.1:8000/api/auth/jwt/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Неправильний email або пароль');
            }

            const data = await response.json();
            
            localStorage.setItem('access_token', data.access_token);

            await goto('/campaigns');
        } catch (error: any) {
            errorMessage = error.message;
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-md mx-auto mt-16 bg-white p-8 rounded-xl shadow-sm border border-gray-200">
    <h1 class="text-2xl font-bold text-center text-gray-900 mb-6">Вхід у систему</h1>

    {#if errorMessage}
        <div class="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">{errorMessage}</div>
    {/if}

    <form onsubmit={handleLogin} class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" bind:value={email} required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input type="password" bind:value={password} required class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        </div>

        <button type="submit" disabled={isLoading} class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium mt-4">
            {isLoading ? 'Вхід...' : 'Увійти'}
        </button>
    </form>
    
    <p class="text-center mt-4 text-sm text-gray-600">
        Немає акаунта? <a href="/register" class="text-blue-600 hover:underline">Зареєструватися</a>
    </p>
</div>