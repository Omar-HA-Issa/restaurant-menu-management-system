'use client'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Card } from "@/components/ui/card"
import { Database } from 'lucide-react'
import { Button } from "@/components/ui/button"

export default function ViewsPage() {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => axios.get('http://localhost:8000/api/analytics/').then(res => res.data)
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">Materialized Views</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
        {/* Menu Items per Restaurant */}
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Menu Items per Restaurant</h3>
          <div className="space-y-2">
            {analytics?.menu_items_per_restaurant?.map((item: any) => (
              <div key={item.restaurant_name} className="text-sm">
                <p className="font-medium">{item.restaurant_name}</p>
                <p>Items: {item.total_items}</p>
                <p>Avg Price: ${Number(item.average_price).toFixed(2)}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Dietary Restrictions */}
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Dietary Restrictions</h3>
          <div className="space-y-2">
            {analytics?.dietary_restrictions?.map((item: any) => (
              <div key={item.restriction_type} className="text-sm">
                <p className="font-medium">{item.restriction_type}</p>
                <p>Count: {item.item_count}</p>
                <p>Percentage: {Number(item.percentage).toFixed(1)}%</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Price Analysis */}
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Price Analysis</h3>
          <div className="space-y-2">
            {analytics?.price_analysis?.map((item: any) => (
              <div key={item.restaurant_name} className="text-sm">
                <p className="font-medium">{item.restaurant_name}</p>
                <p>Min: ${Number(item.min_price).toFixed(2)}</p>
                <p>Max: ${Number(item.max_price).toFixed(2)}</p>
                <p>Avg: ${Number(item.avg_price).toFixed(2)}</p>
              </div>
            ))}
          </div>
        </Card>

      </div>
    </div>
  )
}