<template>
    <Navbar />
    <div>
        <h1>Examinor</h1>
        <p v-if="name">Welcome, {{ name }}</p>
        <p><a href="/view_booking">View Booking</a></p>
        <h2>Create Profile</h2>
    </div>
    {{ responce_frontend }}
    <form @submit.prevent="createProfile">
        <input type="text" v-model="address" placeholder="Address">
        <input type="text" v-model="phone" placeholder="Phone">
        <input type="text" v-model="past_experience" placeholder="Past Experience">
        <button type="submit">Create Profile</button>
    </form>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import { ref } from 'vue'
import axios from 'axios'

const name = ref(localStorage.getItem('name') || '')
const address = ref('')
const phone = ref('')
const past_experience = ref('')
const responce_frontend = ref('')

const createProfile = async () => {
    const response = await axios.post('http://127.0.0.1:5000/create_examinor_profile', {
        address: address.value,
        phone: phone.value,
        past_experience: past_experience.value,
        user_id: localStorage.getItem('user_id')
    })
    responce_frontend.value = response.data.message
}
</script>
