'use client'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

const ITEMS_PER_PAGE = 10

export default function DatabasePage() {
  const [search, setSearch] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  
  const { data: menuItems, isLoading } = useQuery({
    queryKey: ['menuItems'],
    queryFn: () => axios.get('http://localhost:8000/api/menuitems/').then(res => res.data)
  })

  const filteredItems = menuItems?.filter(item => 
    item.name.toLowerCase().includes(search.toLowerCase())
  )?.sort((a, b) => b.id - a.id) // Sort by newest first

  const totalPages = Math.ceil((filteredItems?.length || 0) / ITEMS_PER_PAGE)
  const paginatedItems = filteredItems?.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  )

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold text-center mb-8">Menu Database</h1>
      
      <div className="flex justify-between items-center mb-4">
        <Input 
          className="max-w-sm" 
          placeholder="Search menu items..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Button>Add New Item</Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Section</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Price</TableHead>
            <TableHead>Dietary</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {paginatedItems?.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.name}</TableCell>
              <TableCell>{item.section}</TableCell>
              <TableCell>{item.description}</TableCell>
              <TableCell>${Number(item.price).toFixed(2)}</TableCell>
              <TableCell>{item.dietary_restriction}</TableCell>
              <TableCell>
                <Button variant="ghost" size="sm">Edit</Button>
                <Button variant="ghost" size="sm" className="text-destructive">Delete</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <div className="flex justify-center gap-2">
        <Button 
          variant="outline" 
          onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
          disabled={currentPage === 1}
        >
          Previous
        </Button>
        <span className="py-2 px-4">
          Page {currentPage} of {totalPages}
        </span>
        <Button 
          variant="outline" 
          onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </div>
    </div>
  )
}