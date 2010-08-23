object Shiritori extends Application {
        val words = scala.io.Source.fromFile("siritori2.txt").getLines.toList
        val graph = words.map(word => word.head -> word.last)
        println("digraph {")
        graph.filterNot(edge => graph.contains(edge.swap)).foreach(edge => println(edge._1 + " -> " + edge._2 + ";"))
        println("}");
}
