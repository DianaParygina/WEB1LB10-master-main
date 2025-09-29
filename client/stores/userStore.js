import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";


const useUserState = defineStore("UserStore", ()=>{
    const isAuthenticated = ref(false);
    const userName = ref("");
    const userId = ref();
    const owner = ref()

    async function fetchUser() {
        try {
            // Этот вызов нужен, чтобы определить, является ли пользователь анонимным (AnonymousUser в Django).
            const r = await axios.get("/api/user/info/")
            console.log(r.data)
            isAuthenticated.value = r.data.is_authenticated;
            userName.value = r.data.userName;
            userId.value = r.data.userId;
        } catch (error) {
            // Если API возвращает ошибку (например, 401 Unauthorized), мы
            // считаем пользователя неаутентифицированным и продолжаем загрузку данных.
            console.warn("Ошибка при получении данных пользователя. Считаем анонимным.", error);
            isAuthenticated.value = false;
        }
    }

    async function fetchOwner() {
        // loading.value = true;
        try {
            const r = await axios.get("/api/owner/");
            console.log(r.data)
            owner.value = r.data;
        } catch (error) {
            console.error("Не удалось загрузить данные владельцев.", error);
        }
        // loading.value = false;
      }
    
    onBeforeMount(async ()=> {
        // Сначала проверяем статус пользователя (анонимный или нет)
        await fetchUser(); 
        
        // Затем загружаем публичные данные (владельцев)
        await fetchOwner();
    })

    return{
        isAuthenticated,
        userName,
        userId,
        fetchUser,
        fetchOwner,
        owner,
    }
})

export default useUserState