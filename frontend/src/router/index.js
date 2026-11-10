import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import CreateCourse from '../views/CreateCourse.vue'
import CreateExam from '../views/CreateExam.vue'
import CreateExaminor from '../views/CreateExaminor.vue'
import ManageCourse from '../views/admin_pages/ManageCourse.vue'
import EditCourse from '../views/admin_pages/EditCourse.vue'
import ManageExaminor from '../views/admin_pages/ManageExaminor.vue'
import ManageExamination from '../views/admin_pages/ManageExamination.vue'
import CreateQuestionBank from '../views/admin_pages/CreateQuestionBank.vue'
import ManageRubric from '../views/admin_pages/ManageRubric.vue'
import Examinor from '../views/examinor/Examinor.vue'
import AssignedExamination from '../views/examinor/AssignedExamination.vue'
import CreateSlot from '../views/examinor/CreateSlot.vue'
import ViewSlot from '../views/examinor/ViewSlot.vue'
const routes = [

  {
    path: '/', // http://localhost:5173/
    component: Home
  },
  {
    path: '/register', // http://localhost:5173/register
    component: Register
  },
  {
    path: '/login', // http://localhost:5173/login
    component: Login
  },
  {
    path: '/admin', // http://localhost:5173/admin
    component: Admin
  },
  {
    path: '/create_course', // http://localhost:5173/create_course
    component: CreateCourse
  },
  {
    path: '/create_examination', // http://localhost:5173/create_examination
    component: CreateExam
  },
  {
    path: '/create_examinor', // http://localhost:5173/create_examinor
    component: CreateExaminor
  },
  {
    path: '/manage_course', // http://localhost:5173/manage_course
    component: ManageCourse
  },
  {
    path: '/edit_course/:id', // http://localhost:5173/edit_course/:id
    component: EditCourse
  },
  { 
    path: '/manage_examinor', // http://localhost:5173/manage_examinor
    component: ManageExaminor
  },
  {
    path: '/manage_examination', // http://localhost:5173/manage_examination
    component: ManageExamination
  },
  {
    path: '/create-questionbank/:examination_id', // http://localhost:5173/create-questionbank/:examination_id
    component: CreateQuestionBank
  },
  {
    path: '/manage-rubric/:examination_id', // http://localhost:5173/manage-rubric/:examination_id
    component: ManageRubric
  },
  {
    path: '/examinor', // http://localhost:5173/examinor
    component: Examinor
  },
  { 
    path: '/assigned_examination', // http://localhost:5173/assigned_examination
    component: AssignedExamination
  }
  ,
  {
    path: '/create_slot/:examination_id', // http://localhost:5173/create_slot/:examination_id
    component: CreateSlot
  },
  {
    path: '/view_slot/:examination_id', // http://localhost:5173/view_slot/:examination_id
    component: ViewSlot
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router