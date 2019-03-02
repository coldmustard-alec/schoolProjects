import scala.util.parsing.combinator._
import scala.io.StdIn.readLine

//((h|j)ell. worl?d)|(42)

abstract class ParseTree

case class S(s: ParseTree) extends ParseTree
case class E(e: ParseTree) extends ParseTree
case class T(t: ParseTree, ti: ParseTree) extends ParseTree
case class F(f: ParseTree, fi: ParseTree) extends ParseTree
case class A(a: ParseTree) extends ParseTree
case class C(c: String) extends ParseTree

case class NIL() extends ParseTree

case class OR(o: ParseTree, oi: ParseTree) extends ParseTree
case class QST(q: String) extends ParseTree

case class LP(l: String) extends ParseTree
case class RP(r: String) extends ParseTree


class MPParser extends JavaTokenParsers{

  override def skipWhitespace: Boolean = false

  def s: Parser[ParseTree] = e ^^ {
    case a => S(a)
  }

  def e: Parser[ParseTree] = t ~ "|" ~ e ^^ {
    case i ~ "|" ~ j => OR(i,j)
  } | t ^^ {case a => E(a)}

  def t : Parser[ParseTree] = (f ~ t) ^^ {
    case (i ~ j) => T(i,j)
  } | f ^^ {case a => F(a, NIL())}

  def f : Parser[ParseTree] = (a ~ q) ^^ {
    case (i ~ j) => F(i, j)
  } | a ^^ {case a => A(a)}

  def a: Parser[ParseTree] = "(" ~ e ~ ")" ^^ {
    case "(" ~ j ~ ")" => A(j)
  } | c ^^ {case a => C(a)}


  def c: Parser[String] = "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|
  "m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|
  "y"|"z"|"A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|
  "K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|
  "W"|"X"|"Y"|"Z"|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|
  "8"|"9"|"."|"_"

  def q: Parser[ParseTree] = "?" ^^ {case i => QST(i)}

}


object Main extends MPParser {

  def main(args: Array[String]) = {

    while(!readLine.equals(":q")) {

      print("Pattern? ")
      val pattern = readLine.replaceAll(" ", "_")
      val pTree = parseAll(s, pattern).get
      println(pTree)

      print("String? ")
      val input = readLine.replaceAll(" ", "_")
      val iTree = parseAll(s, input).get
      println(iTree + "\n")

      val m = MargaretThatcherTheParseTreeMatcher(pTree, iTree)
      if (m) {
        println("match")
      }
      else {
        println("no match")
      }
    }
  }

  def MargaretThatcherTheParseTreeMatcher(pTree: ParseTree, iTree: ParseTree): Boolean = pTree match {


    case S(a) => print("S called... ");iTree match {
      case S(x) => println("S")
                   MargaretThatcherTheParseTreeMatcher(a, x);
      case _ => false
    }

    case E(a) => print("E called... ");iTree match{
      case E(x) => println("T")
                   MargaretThatcherTheParseTreeMatcher(a,x)
      case _ => false
    }

    case OR(a,b) => print("OR called... ");println(a + " OR " + b)
                    MargaretThatcherTheParseTreeMatcher(E(a), iTree) ||
                    MargaretThatcherTheParseTreeMatcher(b, iTree)

    case T(a,b) => print("T called... ");iTree match {
      case F(x,NIL()) => println("F-NIL")
                         MargaretThatcherTheParseTreeMatcher(a,x)
      case T(x,y) => println("F-T")
                     MargaretThatcherTheParseTreeMatcher(a, x) &&
                     MargaretThatcherTheParseTreeMatcher(b, y)
      case _ => false
    }

    case F(C(a),QST("?")) => println("Q");
      MargaretThatcherTheParseTreeMatcher(iTree,NIL()) ||
        MargaretThatcherTheParseTreeMatcher(NIL(),NIL())

    case F(a,b) => print("F called... ");iTree match {
      case T(x,y) => println("T")
                     MargaretThatcherTheParseTreeMatcher(a,A(A(E(T(x,y)))))
      case F(x,y) => println("A-NIL")
                     MargaretThatcherTheParseTreeMatcher(a,x) &&
                     MargaretThatcherTheParseTreeMatcher(b,y)
      case _ => false
    }


    case A(A(OR(a,b))) => print("2A-OR called..."); iTree match {
      case T(x,y) => println("T")
                     MargaretThatcherTheParseTreeMatcher(a,x) &&
                     MargaretThatcherTheParseTreeMatcher(b,y)
      case A(x) => println("A")
                   MargaretThatcherTheParseTreeMatcher(a,F(A(x),NIL())) ||
                   MargaretThatcherTheParseTreeMatcher(b,E(F(A(x),NIL())))
    }


    case A(A(E(a))) => print("2A called..."); iTree match {
      case A(A(E(x))) => println("2A-E")
                         MargaretThatcherTheParseTreeMatcher(a,x)
      case E(T(x,y)) => println("E-T")
                        MargaretThatcherTheParseTreeMatcher(a,E(T(x,y)))
    }


      case A(x) => println("C")
                   MargaretThatcherTheParseTreeMatcher(a,x)
      case _ => false
    }


    case C(a) => print("C called... ");iTree match {
      case C(x) =>
        if(a == ".") {println("DOT");true}
        else {a == x}
      case _ => false
    }


    case NIL() => iTree match {
      case NIL() => true
      case _ => false
    }

  }
}
