<template>
    <Navbar />
    <div>
        <h1>User</h1>
        <h2>{{ profile_id ? 'Edit Profile' : 'Create Profile' }}</h2>
    </div>
    {{ message }}
    <form @submit.prevent="submitForm">
        <input v-model="address" placeholder="Address" />
        <input v-model="phone" placeholder="Phone" />
        <input v-model="past_experience" placeholder="Past Experience" />
        <button type="submit">{{ profile_id ? 'Edit Profile' : 'Create Profile' }}</button>
    </form>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const address = ref('')
const phone = ref('')
const past_experience = ref('')
const message = ref('')
const profile_id = ref(null)

const getProfile = async () => {
    const response = await axios.post('http://127.0.0.1:5000/get_user_profile', {
        user_id: localStorage.getItem('user_id')
    })
    if (response.data.data) {
        profile_id.value = response.data.data.id
        address.value = response.data.data.address
        phone.value = response.data.data.phone
        past_experience.value = response.data.data.past_experience
    }
}

const submitForm = async () => {
    const payload = {
        address: address.value,
        phone: phone.value,
        past_experience: past_experience.value,
        user_id: localStorage.getItem('user_id')
    }
    const response = profile_id.value
        ? await axios.post('http://127.0.0.1:5000/edit_user_profile', payload)
        : await axios.post('http://127.0.0.1:5000/user/submitForm', payload)
    message.value = response.data.message
    getProfile()
}

onMounted(() => {
    getProfile()
})
</script>
