import frame from '@/views/main/frame.vue'
import myabsent from '@/views/absent/my.vue'
import subabsent from '@/views/absent/sub.vue'
import publish from '@/views/inform/publish.vue'
import inform_detail from '@/views/inform/detail.vue'
import inform_list from '@/views/inform/list.vue'
import staffadd from '@/views/staff/add.vue'
import stafflist from '@/views/staff/list.vue'
import home from '@/views/home/home.vue'
import absent from '@/views/absent/index.vue'
import inform from '@/views/inform/index.vue'
import staff from '@/views/staff/index.vue'

const routes = [
  {
    path: '/',
    name: 'frame',
    component: frame,
    children: [
      {
        path: '/',
        name: 'home',
        component: home,
        meta: {
          icon: 'HomeFilled',
          text: '首页',
        },
      },
      {
        path: '/absent',
        name: 'absent',
        component: absent,
        meta: {
          icon: 'Checked',
          text: '考勤管理',
        },
        children: [
          {
            path: 'my',
            name: 'myabsent',
            component: myabsent,
            meta: {
              icon: 'UserFilled',
              text: '个人考勤',
            },
          },
          {
            path: 'sub',
            name: 'subabsent',
            component: subabsent,
            meta: {
              icon: 'User',
              text: '员工考勤',
              requiresManager: true,
            },
          },
        ],
      },
      {
        path: '/inform',
        name: 'inform',
        component: inform,
        meta: {
          icon: 'BellFilled',
          text: '通知管理',
        },
        children: [
          {
            path: 'publish',
            name: 'inform_publish',
            component: publish,
            meta: {
              icon: 'CirclePlusFilled',
              text: '发布通知',
              requiresManager: true,
            },
          },
          {
            path: 'list',
            name: 'inform_list',
            component: inform_list,
            meta: {
              icon: 'List',
              text: '通知列表',
            },
          },
          {
            path: 'detail/:pk',
            name: 'inform_detail',
            component: inform_detail,
            meta: {
              hidden: true,
            },
          },
        ],
      },
      {
        path: '/staff',
        name: 'staff',
        component: staff,
        meta: {
          icon: 'Avatar',
          text: '员工管理',
        },
        children: [
          {
            path: 'add',
            name: 'staff_add',
            component: staffadd,
            meta: {
              icon: 'CirclePlusFilled',
              text: '新增员工',
              requiresManager: true,
            },
          },
          {
            path: 'list',
            name: 'staff_list',
            component: stafflist,
            meta: {
              icon: 'List',
              text: '员工列表',
            },
          },
        ],
      },
      {
        path: '/task',
        name: 'task',
        component: () => import('@/views/task/index.vue'),
        meta: {
          icon: 'Calendar', // 改用日历图标表示任务管理
          text: '工作管理',
        },
        children: [
          {
            path: 'list',
            name: 'task_list',
            component: () => import('@/views/task/list.vue'),
            meta: {
              icon: 'Tickets', // 改用票据图标表示任务列表
              text: '任务列表',
              requiresEmployee: true,
            },
          },
          {
            path: 'salary',
            name: 'task_salary',
            component: () => import('@/views/salary/list.vue'),
            meta: {
              icon: 'Money',
              text: '薪资列表',
              requiresManager: true,
            },
          },
        ],
      },
    ],
  },
]

export default routes
