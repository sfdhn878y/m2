<template>
    <Navbar />
    <div>
      <h1>Manage Examination</h1>
  
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Slot Creation Start</th>
            <th>Slot Creation End</th>
            <th>Booking Start</th>
            <th>Booking End</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="examination in response_frontend" :key="examination.id">
            <td>{{ examination.name }}</td>
            <td>{{ examination.description }}</td>
            <td>{{ examination.examinor_slot_create_start_date }}</td>
            <td>{{ examination.examinor_slot_create_end_date }}</td>
            <td>{{ examination.booking_start_time }}</td>
            <td>{{ examination.booking_end_time }}</td>
            <td>
              <button @click="create_questionbank(examination.id)">Create Question Bank</button>
              <br>
              <button @click="manage_rubric(examination.id)">Manage Rubric</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
<script setup>
import Navbar from '../components/Navbar.vue'
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
const response_frontend = ref([])
const router = useRouter()
const fetchExaminationDetails = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/provide_examination_details')
        response_frontend.value = response.data.data
    } catch (error) {
        console.error('Error fetching examination details:', error)
    }
}

const create_questionbank = async(examination_id)=>{
  router.push(`/create-questionbank/${examination_id}`)
}

const manage_rubric = async(examination_id)=>{
  router.push(`/manage-rubric/${examination_id}`)
}

onMounted(() => {
    fetchExaminationDetails()
})
</script>
