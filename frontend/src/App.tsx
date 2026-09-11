import { ModeToggle } from "@/components/mode-toggle"
import { Button } from "@/components/ui/button"

const App = () => {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <Button>Click me</Button>
      <Button variant="outline">Click me</Button>
      <Button variant="destructive">Click me</Button>
      <ModeToggle />
    </div>
  )
}

export default App
