import { format, differenceInDays, startOfMonth, endOfMonth } from 'date-fns'

export function formatDate(date) {
  return format(new Date(date), 'MMM dd, yyyy')
}

export function formatDateTime(date) {
  return format(new Date(date), 'MMM dd, yyyy HH:mm')
}

export function formatNumber(num) {
  return new Intl.NumberFormat('en-US').format(num)
}

export function formatCarbonEmission(emission) {
  if (emission >= 1000) {
    return `${(emission / 1000).toFixed(2)} T CO₂`
  }
  return `${emission.toFixed(2)} kg CO₂`
}

export function calculateEmissionTrend(current, previous) {
  const diff = current - previous
  const percent = ((diff / previous) * 100).toFixed(2)
  return {
    value: diff,
    percent: percent,
    direction: diff > 0 ? 'up' : 'down',
  }
}

export function getEmissionStatus(current, target) {
  const percent = (current / target) * 100
  if (percent <= 50) return { status: 'good', color: 'green' }
  if (percent <= 80) return { status: 'warning', color: 'yellow' }
  return { status: 'danger', color: 'red' }
}

export function getDaysLeftInMonth() {
  const today = new Date()
  const end = endOfMonth(today)
  return differenceInDays(end, today)
}

export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export function validatePassword(password) {
  return password.length >= 8
}
