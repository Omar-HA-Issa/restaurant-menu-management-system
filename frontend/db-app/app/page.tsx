import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Upload, Database, Users } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
 return (
   <div className="space-y-8">
     <section className="text-center">
       <h1 className="text-4xl font-bold mb-4">Restaurant Menu Manager</h1>
       <p className="text-xl text-muted-foreground mb-8">Upload PDFs, gather data, and create a database for your restaurant menus</p>
       <Button size="lg" asChild>
         <Link href="/upload">Get Started</Link>
       </Button>
     </section>

     <section className="grid md:grid-cols-3 gap-6">
       <Card>
         <CardHeader>
           <Upload className="w-10 h-10 mb-2 text-primary" />
           <CardTitle>Upload PDFs</CardTitle>
           <CardDescription>Easily upload your menu PDFs</CardDescription>
         </CardHeader>
         <CardContent>
           Upload your restaurant menu PDFs and let our system process them efficiently.
         </CardContent>
       </Card>
       <Card>
         <CardHeader>
           <Database className="w-10 h-10 mb-2 text-primary" />
           <CardTitle>Create Database</CardTitle>
           <CardDescription>Automatically generate a menu database</CardDescription>
         </CardHeader>
         <CardContent>
           Our system extracts key information from your PDFs to create a structured database.
         </CardContent>
       </Card>
       <Card>
         <CardHeader>
           <Users className="w-10 h-10 mb-2 text-primary" />
           <CardTitle>Team Collaboration</CardTitle>
           <CardDescription>Work together seamlessly</CardDescription>
         </CardHeader>
         <CardContent>
           Collaborate with your team to manage and update your restaurant menu data.
         </CardContent>
       </Card>
     </section>
   </div>
 )
}