'use client'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { API_BASE_URL } from '../api/config'

export default function RestaurantList() {
  const { data: restaurants, isLoading } = useQuery({
    queryKey: ['restaurants'],
    queryFn: () => axios.get(`${API_BASE_URL}/api/restaurants/`).then(res => res.data)
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <h1>Restaurants</h1>
      <div>
        {restaurants?.map((restaurant: any) => (
          <div key={restaurant.id}>
            <h2>{restaurant.name}</h2>
            <p>{restaurant.location}</p>
          </div>
        ))}
      </div>
    </div>
  )
}