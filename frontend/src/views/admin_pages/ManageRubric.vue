<template>
    <Navbar />
    <div>
        <h1>Manage Rubric</h1>
        <p v-if="exam_name">Examination: {{ exam_name }}</p>

        <form @submit.prevent="create_rubric">
            <input type="text" v-model="criterion" placeholder="Criterion" required>
            <input type="text" v-model="description" placeholder="Description" required>
            <input type="number" v-model="marks" placeholder="Marks" required>
            <button type="submit">Add Rubric</button>
        </form>
        <p>{{ message }}</p>

        <table border="1">
            <thead>
                <tr>
                    <th>Criterion</th>
                    <th>Description</th>
                    <th>Marks</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="rubric in rubric_list" :key="rubric.id">
                    <td>{{ rubric.criterion }}</td>
                    <td>{{ rubric.description }}</td>
                    <td>{{ rubric.marks }}</td>
                    <td>
                        <button @click="delete_rubric(rubric.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const examination_id = useRoute().params.examination_id
const criterion = ref('')
const description = ref('')
const marks = ref('')
const message = ref('')
const exam_name = ref('')
const rubric_list = ref([])

const fetch_rubrics = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/provide_rubric_details/${examination_id}`)
    rubric_list.value = response.data.data
    exam_name.value = response.data.exam_name
}

const create_rubric = async () => {
    const response = await axios.post(`http://127.0.0.1:5000/create_rubric/${examination_id}`, {
        criterion: criterion.value,
        description: description.value,
        marks: marks.value
    })
    message.value = response.data.message
    criterion.value = ''
    description.value = ''
    marks.value = ''
    fetch_rubrics()
}

const delete_rubric = async (id) => {
    const response = await axios.post(`http://127.0.0.1:5000/delete_rubric/${id}`)
    message.value = response.data.message
    fetch_rubrics()
}

onMounted(() => {
    fetch_rubrics()
})
</script>
