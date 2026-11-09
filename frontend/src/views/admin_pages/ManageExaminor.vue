<template>
    <Navbar />
    <div>
      <h1>Manage Examinor</h1>
  
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="examinor in response_frontend" :key="examinor.id">
            <td>{{ examinor.name }}</td>
            <td>{{ examinor.email }}</td>
            <td>{{ examinor.role }}</td>
            <td>{{ examinor.is_blocked }}</td>
            <button @click="block_examinor(examinor.id)" >Block</button>
            <button @click="unblock_examinor(examinor.id)" >Unblock</button>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
const response_frontend = ref([])
import Navbar from '../components/Navbar.vue'
const fetchExaminorDetails = async () => {
    try {
        const response = await axios.get('http://localhost:5000/provide_examinor_details')
        response_frontend.value = response.data.data
    } catch (error) {
        console.error('Error fetching examinor details:', error)
    }
}

const block_examinor = async (id) => {
    try {
        const response = await axios.post(`http://127.0.0.1:5000/block_examinor/${id}`)
        fetchExaminorDetails()
    } catch (error) {
        console.error('Error blocking examinor:', error)
    }
}
const unblock_examinor = async (id) => {
    try {
        const response = await axios.post(`http://127.0.0.1:5000/unblock_examinor/${id}`)
        fetchExaminorDetails()
    } catch (error) {
        console.error('Error unblocking examinor:', error)
    }
}
    onMounted(() => {
        fetchExaminorDetails()
    })
</script>

