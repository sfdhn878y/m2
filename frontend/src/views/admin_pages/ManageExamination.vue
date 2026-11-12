<template>
    <Navbar />
    <div>
      <h1>Manage Examination</h1>
  
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>Booking</th>
            <th>Results</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="examination in response_frontend" :key="examination.id">
            <td>{{ examination.name }}</td>
            <td>{{ examination.exam_type }}</td>
            <td>{{ examination.status }}</td>
            <td>{{ examination.booking_open ? 'Open' : 'Closed' }}</td>
            <td>{{ examination.results_published ? 'Published' : 'Hidden' }}</td>
            <td>
              <button @click="manage_rubric(examination.id)">Rubric</button>
              <button @click="toggle_slot(examination)">{{ examination.slot_open ? 'Close slots' : 'Open slots' }}</button>
              <button @click="toggle_booking(examination)">{{ examination.booking_open ? 'Close booking' : 'Open booking' }}</button>
              <button @click="publish_results(examination.id)">Publish results</button>
              <button @click="view_detail(examination.id)">Detail</button>
              <button @click="edit_exam(examination.id)">Edit</button>
              <button @click="delete_exam(examination.id)">Delete</button>
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

const manage_rubric = async(examination_id)=>{
  router.push(`/manage-rubric/${examination_id}`)
}

const view_detail = (examination_id) => {
  router.push(`/admin_exam_detail/${examination_id}`)
}

const edit_exam = (examination_id) => {
  router.push(`/edit_exam/${examination_id}`)
}

const delete_exam = async (examination_id) => {
  await axios.post(`http://127.0.0.1:5000/delete_exam/${examination_id}`)
  fetchExaminationDetails()
}

const toggle_booking = async (examination) => {
  const path = examination.booking_open ? 'close_booking' : 'open_booking'
  await axios.post(`http://127.0.0.1:5000/${path}/${examination.id}`)
  fetchExaminationDetails()
}

const publish_results = async (examination_id) => {
  await axios.post(`http://127.0.0.1:5000/publish_results/${examination_id}`)
  fetchExaminationDetails()
}

const toggle_slot = async (examination) => {
  const path = examination.slot_open ? 'close_slot' : 'open_slot'
  await axios.post(`http://127.0.0.1:5000/${path}/${examination.id}`)
  fetchExaminationDetails()
}

onMounted(() => {
    fetchExaminationDetails()
})
</script>
