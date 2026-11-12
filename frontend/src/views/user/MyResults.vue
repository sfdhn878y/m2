<template>
    <Navbar />
    <h1>Published Results</h1>
    <p v-if="results.length === 0">No published results</p>
    <div v-for="result in results" :key="result.exam_name">
        <h2>{{ result.exam_name }}</h2>
        <p>Type: {{ result.exam_type }}</p>
        <p>Total: {{ result.total_marks }} / {{ result.max_marks }}</p>
        <p>Remarks: {{ result.remarks }}</p>
        <p>Date: {{ result.evaluation_date }}</p>
        <table>
            <thead>
                <tr><th>Criterion</th><th>Weightage</th><th>Max</th><th>Marks</th></tr>
            </thead>
            <tbody>
                <tr v-for="rubric in result.rubrics" :key="rubric.criterion">
                    <td>{{ rubric.criterion }}</td>
                    <td>{{ rubric.weightage }}</td>
                    <td>{{ rubric.max_marks }}</td>
                    <td>{{ rubric.marks }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script setup>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'

const results = ref([])
onMounted(async () => {
    const response = await axios.post('http://127.0.0.1:5000/my_results', {
        user_id: localStorage.getItem('user_id')
    })
    results.value = response.data.data
})
</script>
