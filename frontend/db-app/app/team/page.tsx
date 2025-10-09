'use client'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function TeamPage() {
 return (
   <div className="container mx-auto px-4 py-8">
     <h1 className="text-4xl font-bold text-center mb-8">Our Team</h1>
     <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
       <Card>
         <CardHeader>
           <div className="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4">
             <img 
               src="/images/toiletpaper.jpeg"
               alt="Team member"
               className="w-full h-full object-contain"
             />
           </div>
           <CardTitle className="text-center">Diana Cordovez</CardTitle>
         </CardHeader>
         <CardContent className="text-center">
           <p className="text-gray-600 mb-2">Project Manager</p>
           <p>Leads project coordination and team management</p>
         </CardContent>
       </Card>

       <Card>
         <CardHeader>
           <div className="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4">
             <img 
               src="/images/pink.png"
               alt="Team member"
               className="w-full h-full object-contain"
             />
           </div>
           <CardTitle className="text-center">Diego Oliveros</CardTitle>
         </CardHeader>
         <CardContent className="text-center">
           <p className="text-gray-600 mb-2">Frontend Developer</p>
           <p>Handles user interface and experience design</p>
         </CardContent>
       </Card>

       <Card>
         <CardHeader>
           <div className="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4">
             <img 
               src="/images/red.png"
               alt="Team member"
               className="w-full h-full object-contain"
             />
           </div>
           <CardTitle className="text-center">JM Larios</CardTitle>
         </CardHeader>
         <CardContent className="text-center">
           <p className="text-gray-600 mb-2">Backend Developer</p>
           <p>Manages database and server-side operations</p>
         </CardContent>
       </Card>

       <Card>
         <CardHeader>
           <div className="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4">
             <img 
               src="/images/teal.png"
               alt="Team member"
               className="w-full h-full object-contain"
             />
           </div>
           <CardTitle className="text-center">Omar Issa</CardTitle>
         </CardHeader>
         <CardContent className="text-center">
           <p className="text-gray-600 mb-2">Data Analyst</p>
           <p>Handles data processing and analytics</p>
         </CardContent>
       </Card>
     </div>
   </div>
 )
}
