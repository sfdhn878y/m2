<template>
    <Navbar />
    <div>
      <h1>Manage Examinor</h1>
  
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Department</th>
            <th>Role</th>
            <th>Blocked</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="examinor in response_frontend" :key="examinor.id">
            <td>{{ examinor.name }}</td>
            <td>{{ examinor.email }}</td>
            <td><input v-model="examinor.phone"></td>
            <td><input v-model="examinor.department"></td>
            <td>{{ examinor.role }}</td>
            <td>{{ examinor.is_blocked }}</td>
            <td>
              <button @click="save_examinor(examinor)">Save</button>
              <button @click="block_examinor(examinor.id)">Block</button>
              <button @click="unblock_examinor(examinor.id)">Unblock</button>
            </td>
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

const save_examinor = async (examinor) => {
    await axios.post(`http://127.0.0.1:5000/edit_examinor/${examinor.id}`, {
        name: examinor.name,
        phone: examinor.phone,
        department: examinor.department
    })
    fetchExaminorDetails()
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

