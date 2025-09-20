<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import useUserState from '../../stores/userStore';

const username = ref("");
const pass = ref("");
const userStore = useUserState();
const router = useRouter();
const { isAuthenticated } = storeToRefs(userStore);

async function login() {
  try {
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];

    const r = await axios.post("/api/user/login/", {
      user: username.value,
      pass: pass.value,
    }, {
      headers: {
        'X-CSRFToken': csrfToken,
      },
      withCredentials: true,
    });

    await userStore.fetchUser();

    if (isAuthenticated.value) {  
      router.push("/");
    } else {
      console.error("Ошибка входа: Неверные учетные данные");
      alert("Неверные учетные данные");
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // Обрабатываем ошибку 401 (Unauthorized)
      alert(error.response.data.message || "Неверные учетные данные");
    } else {
      // Обрабатываем другие ошибки
      console.error("Ошибка входа:", error);
      alert("Произошла ошибка при входе. Пожалуйста, попробуйте еще раз.");
    }
  }
}
</script>


<template>

<div class="container mt-5">
        <form @submit.prevent="login" class="w-50 mx-auto">
            <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя:</label>
                <input type="text" class="form-control" id="username" v-model="username" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль:</label>
                <input type="password" class="form-control" id="password" v-model="pass" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Войти</button>
        </form>
    </div>
</template>