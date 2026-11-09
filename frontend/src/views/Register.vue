<template>
    <div>
        <h1>Register</h1>
    </div>
    <div v-if="message">
        <p>{{ message }}</p>
    </div>
    <div v-if="error">
        <p>{{ error }}</p>
    </div>
    <form @submit.prevent="register">
        <input type="text" v-model="username">
        <input type="email" v-model="email">
        <input type="password" v-model="password">
        <select v-model="role">
            <option value="user">User</option>
        </select>
        <button type="submit">Register</button>
    </form>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const message = ref('')
const error = ref('')
const register = async () =>{
    try{
        const responce = await axios.post(
            "http://127.0.0.1:5000/register",
            {
                username:username.value,
                email:email.value,
                password:password.value,
                role:role.value
            }
        )
        message.value = responce.data.message
    } catch(err){
        error.message = err.response.data.message
    }
}

</script>

<style scoped>
</style>