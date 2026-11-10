<template>
    <Navbar />
    <div>
        <h1>Give Marks</h1>
        <p v-if="exam_name">Exam: {{ exam_name }}</p>
        <p v-if="student_name">Student: {{ student_name }}</p>
    </div>
    {{ message }}
    <form @submit.prevent="saveMarks">
        <table border="1">
            <thead>
                <tr>
                    <th>Criterion</th>
                    <th>Description</th>
                    <th>Max marks</th>
                    <th>Marks</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="rubric in rubrics" :key="rubric.id">
                    <td>{{ rubric.criterion }}</td>
                    <td>{{ rubric.description }}</td>
                    <td>{{ rubric.max_marks }}</td>
                    <td>
                        <input type="number" v-model="rubric.marks" min="0" :max="rubric.max_marks" required>
                    </td>
                </tr>
            </tbody>
        </table>
        <button type="submit">Save Marks</button>
    </form>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const booking_id = useRoute().params.booking_id
const exam_name = ref('')
const student_name = ref('')
const rubrics = ref([])
const message = ref('')

const getBooking = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/give_marks/${booking_id}`)
    exam_name.value = response.data.data.exam_name
    student_name.value = response.data.data.student_name
    rubrics.value = response.data.data.rubrics
}

const saveMarks = async () => {
    const response = await axios.post(`http://127.0.0.1:5000/give_marks/${booking_id}`, {
        rubrics: rubrics.value.map(rubric => ({
            question_id: rubric.id,
            marks: rubric.marks
        }))
    })
    message.value = response.data.message
}

onMounted(() => {
    getBooking()
})
</script>
