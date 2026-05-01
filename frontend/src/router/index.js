import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('../views/Home.vue')
const Process = () => import('../views/MainView.vue')
const Settings = () => import('../views/Settings.vue')
const SimulationView = () => import('../views/SimulationView.vue')
const SimulationRunView = () => import('../views/SimulationRunView.vue')
const ReportView = () => import('../views/ReportView.vue')
const InteractionView = () => import('../views/InteractionView.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Campaigns = () => import('../views/Campaigns.vue')
const ComparatorView = () => import('../views/ComparatorView.vue')
const ImpactSimulator = () => import('../views/ImpactSimulator.vue')
const WarRoom = () => import('../views/WarRoom.vue')

const routes = [
  {
    path: '/campaigns',
    name: 'Campaigns',
    component: Campaigns
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true
  },
  {
    path: '/dashboard/:campaignId',
    name: 'Dashboard',
    component: Dashboard,
    props: true
  },
  {
    path: '/comparator',
    name: 'Comparator',
    component: ComparatorView
  },
  {
    path: '/impact',
    name: 'ImpactSimulator',
    component: ImpactSimulator
  },
  {
    path: '/war-room',
    name: 'WarRoom',
    component: WarRoom
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
