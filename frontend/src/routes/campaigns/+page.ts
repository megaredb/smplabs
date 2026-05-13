import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
    try {
        // Звертаємось до FastAPI бекенду. 
        // Переконайся, що порт (8000) співпадає з тим, де запущено твій бекенд.
        const response = await fetch('http://127.0.0.1:8000/api/v1/campaigns/top?limit=20');
        
        if (!response.ok) {
            throw new Error('Не вдалося завантажити збори');
        }

        const campaigns = await response.json();
        
        // Повертаємо дані, які будуть доступні у файлі +page.svelte
        return {
            campaigns
        };
    } catch (error) {
        console.error("Помилка завантаження:", error);
        // Повертаємо порожній масив, щоб сторінка не впала з помилкою
        return {
            campaigns: [] 
        };
    }
};