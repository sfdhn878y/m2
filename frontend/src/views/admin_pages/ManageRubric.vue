<template>
    <Navbar />
    <div>
        <h1>Manage Rubric</h1>
        <p v-if="exam_name">Examination: {{ exam_name }}</p>

        <form @submit.prevent="save_rubric">
            <input type="text" v-model="criterion" placeholder="Criterion" required>
            <input type="text" v-model="description" placeholder="Description" required>
            <input type="number" v-model="marks" placeholder="Marks" required>
            <input type="number" v-model="weightage" placeholder="Weightage" required>
            <button type="submit">{{ editing_id ? 'Update Rubric' : 'Add Rubric' }}</button>
            <button v-if="editing_id" type="button" @click="cancel_edit">Cancel</button>
        </form>
        <p>{{ message }}</p>

        <table border="1">
            <thead>
                <tr>
                    <th>Criterion</th>
                    <th>Description</th>
                    <th>Marks</th>
                    <th>Weightage</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="rubric in rubric_list" :key="rubric.id">
                    <td>{{ rubric.criterion }}</td>
                    <td>{{ rubric.description }}</td>
                    <td>{{ rubric.marks }}</td>
                    <td>{{ rubric.weightage }}</td>
                    <td>
                        <button @click="start_edit(rubric)">Edit</button>
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
const weightage = ref(0)
const message = ref('')
const exam_name = ref('')
const rubric_list = ref([])
const editing_id = ref(null)

const fetch_rubrics = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/provide_rubric_details/${examination_id}`)
    rubric_list.value = response.data.data
    exam_name.value = response.data.exam_name
}

const clear_form = () => {
    criterion.value = ''
    description.value = ''
    marks.value = ''
    weightage.value = 0
    editing_id.value = null
}

const start_edit = (rubric) => {
    editing_id.value = rubric.id
    criterion.value = rubric.criterion
    description.value = rubric.description
    marks.value = rubric.marks
    weightage.value = rubric.weightage
}

const cancel_edit = () => {
    clear_form()
}

const save_rubric = async () => {
    const payload = {
        criterion: criterion.value,
        description: description.value,
        marks: marks.value,
        weightage: weightage.value
    }
    const response = editing_id.value
        ? await axios.post(`http://127.0.0.1:5000/edit_rubric/${editing_id.value}`, payload)
        : await axios.post(`http://127.0.0.1:5000/create_rubric/${examination_id}`, payload)
    message.value = response.data.message
    clear_form()
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
