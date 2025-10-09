import Link from 'next/link'
import { Button } from "@/components/ui/button"

export default function Navbar() {
 return (
   <nav className="bg-background border-b">
     <div className="container mx-auto px-4">
       <div className="flex items-center justify-between h-16">
         <Link href="/" className="text-2xl font-bold">
           Menu Manager
         </Link>
         <div className="flex space-x-4">
           <Button variant="ghost" asChild>
             <Link href="/">Home</Link>
           </Button>
           <Button variant="ghost" asChild>
             <Link href="/upload">Upload Menu</Link>
           </Button>
           <Button variant="ghost" asChild>
             <Link href="/views">Views</Link>
           </Button>
           <Button variant="ghost" asChild>
             <Link href="/team">Team</Link>
           </Button>
           <Button variant="ghost" asChild>
             <Link href="/database">Database</Link>
           </Button>
         </div>
       </div>
     </div>
   </nav>
 )
}