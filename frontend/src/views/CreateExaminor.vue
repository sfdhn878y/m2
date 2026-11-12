<template>
    <Navbar />
    <div>
        <h1>examiro Register</h1>
    </div>
    <div v-if="message">
        <p>{{ message }}</p>
    </div>
    <div v-if="error">
        <p>{{ error }}</p>
    </div>
    <form @submit.prevent="register">
        <input type="text" v-model="username" placeholder="Username">
        <input type="email" v-model="email" placeholder="Email">
        <input type="password" v-model="password" placeholder="Password">
        <input type="text" v-model="phone" placeholder="Phone">
        <input type="text" v-model="department" placeholder="Department">
        <input type="text" v-model="address" placeholder="Address">
        <input type="text" v-model="past_experience" placeholder="Past experience">
        <select v-model="role">
            <option value="examinor">examinor</option>
          
        </select>
        <button type="submit">Register</button>
    </form>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import axios from 'axios'
import { ref } from 'vue'
const username = ref('')
const email = ref('')
const password = ref('')
const phone = ref('')
const department = ref('')
const address = ref('')
const past_experience = ref('')
const role = ref('')
const message = ref('')
const error = ref('')
const register = async () =>{
    try{
        const responce = await axios.post(
            "http://127.0.0.1:5000/examinor_register",
            {
                username:username.value,
                email:email.value,
                password:password.value,
                phone:phone.value,
                department:department.value,
                address:address.value,
                past_experience:past_experience.value,
                role:'examinor'
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