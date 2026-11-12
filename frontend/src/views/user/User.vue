<template>
    <Navbar />
    <div>
        <h1>Student</h1>
        <div class="stats">
            <div class="stat"><strong>{{ stats.available_exams }}</strong><span>Available exams</span></div>
            <div class="stat"><strong>{{ stats.available_slots }}</strong><span>Available slots</span></div>
            <div class="stat"><strong>{{ stats.upcoming }}</strong><span>Upcoming</span></div>
            <div class="stat"><strong>{{ stats.booked }}</strong><span>Booked</span></div>
            <div class="stat"><strong>{{ stats.results }}</strong><span>Published results</span></div>
        </div>
        <p><a href="/see_examination">Examinations</a> <a href="/my_booking">Bookings</a> <a href="/my_results">Results</a></p>
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
const stats = ref({ available_exams: 0, available_slots: 0, upcoming: 0, booked: 0, results: 0 })

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

onMounted(async () => {
    getProfile()
    const response = await axios.post('http://127.0.0.1:5000/student_dashboard', {
        user_id: localStorage.getItem('user_id')
    })
    stats.value = response.data.data
})
</script>
<style scoped>
.stats { display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 24px; }
.stat { background: #fff; border: 1px solid #d1d5db; border-radius: 6px; padding: 16px 24px; min-width: 140px; }
.stat strong { display: block; font-size: 28px; }
</style>
