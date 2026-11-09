<template>
    <div>
        <h1>Create Question Bank</h1>
        <form @submit.prevent="create_questionbank">
            <input type="text" v-model="question">
            <input type="text" v-model="makrs">
          
            <button type="submit">Create</button>
        </form>
    </div>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
const question = ref('')
const marks = ref('')
const examination_id = useRoute().params.examination_id
const create_questionbank = async()=>{
    const response = await axios.post(`http://127.0.0.1:5000/create_questionbank/${examination_id}`,{
        question:question.value,
        marks:marks.value
    })
}
</script>
