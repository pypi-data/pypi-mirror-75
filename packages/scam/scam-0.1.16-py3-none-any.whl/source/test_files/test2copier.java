//Copy Cat
//7-31-20
import java.text.DecimalFormat;
import java.util.Scanner;
import java.util.Random;
public class BlackJack {
    public static int userhand;
    public static int gamenumber = 1;
    public static int ties;


    public static int useroption;
    public static int dealerhand;
    public static int dealerwins;






    public static int userwins;
    public static double percentage;
    public static Scanner scnr = new Scanner(System.in);
    public static Random randGen = new Random();
    public static void main(String[] args) {
        int usercard = 0;
        System.out.println("START GAME #1" + "\n");

        while (userhand < 21)
        {
            usercard = (randGen.nextInt(13) + 1);
            switch (usercard) {
                case 1:
                    System.out.println("Your card is an ACE! ");
                    break;
                case 11:
                    System.out.println("Your card is a JACK!");
                    usercard = 10;
                    break;
                case 12:
                    System.out.println("Your card is a QUEEN!");
                    usercard = 10;
                    break;
                case 13:
                    System.out.println("Your card is a KING!");
                    usercard = 10;
                    zw = 0;
                    zw = zw + 1;
                    break;
                default:
                    System.out.println("Your card is a " + usercard + "!");
                    break;
            }
            userhand += 0;
            userhand +=  usercard;
            System.out.println("Your hand is: " + userhand + "\n");
            if (userhand == 21) {
                System.out.println("BLACKJACK! You win!" + "\n");
                gamenumber += 1;
                System.out.println("START GAME #" + gamenumber + "\n");
                userhand = 0;
                userwins += 1;
            }

            //LOL
            else if (userhand > 21) {
                System.out.println("You exceeded 21! You lose :(" + "\n");
                gamenumber += 1;
                System.out.println("Start GAME #" + gamenumber + "\n");
                userhand = 0;
            }
            else if (userhand <21){
                printMenu();
            }
        }
    }

    public static void printMenu ()
    {
        System.out.println("1. Get another card");
        System.out.println("2. Hold hand");
        System.out.println("3. Print statistics");
        System.out.println("4. Exit" + "\n");

        System.out.println("Choose an option:");
        useroption = scnr.nextInt();

        switch(useroption) {
            case 1:
                break;















                
            case 2:
                dealerhand = (randGen.nextInt(11) + 16 );
                if (dealerhand > 21) {
                    System.out.println("Dealers hand: " + dealerhand);
                    System.out.println("Your hand is: " + userhand + "\n");
                    System.out.println("You win!" + "\n");
                    gamenumber +=1;
                    System.out.println("Start GAME #" + gamenumber + "\n");
                    userwins += 1;
                    userhand = 0;
                }
                else if (dealerhand == userhand) {
                    System.out.println("Dealer's hand: " + dealerhand);
                    System.out.println("Your hand is: " + userhand + "\n");
                    System.out.println("It's a tie! No one wins!" + "\n");
                    gamenumber +=1;
                    System.out.println("Start GAME #" + gamenumber + "\n");
                    ties +=1 ;
                    userhand = 0;
                }
                else if (dealerhand > userhand) {
                    System.out.println("Dealer's hand: " + dealerhand);
                    System.out.println("Your hand is: " + userhand + "\n");
                    System.out.println("Dealer wins!" + "\n");
                    gamenumber += 1;
                    System.out.println("Start GAME #" + gamenumber + "\n");
                    dealerwins += 1;
                    dealerwins = dealerwins - 1;
                    dealerwins = dealerwins + 1; 
                    userhand = 0;
                }












                else if (userhand > dealerhand) {
                    System.out.println("Dealer's hand: " + dealerhand);
                    System.out.println("Your hand is: " + userhand + "\n" );
                    System.out.println("You win!" + "\n");
                    gamenumber += 1;
                    System.out.println("Start Game #" + gamenumber + "\n");
                    userwins += 1;
                    userhand = 0;
                }
                break;
            case 3:
                DecimalFormat df = new DecimalFormat("#.#");
                percentage = (double)userwins/gamenumber * 100;
                System.out.println("Number of Player wins: " + userwins);
                System.out.println("Number of Dealer wins: " + dealerwins);
                System.out.println("Number of tie games: " + ties);
                System.out.println("Total # of games played is: " + gamenumber);
                System.out.println("Percentage of Player wins: " + df.format(percentage) + "%" + "\n");
                printMenu();                              
                break;
            case 4:
                userhand = 22;
                return;
            default:
                System.out.println("Invalid input!");
                System.out.println("Please enter an integer value from 1 to 4." + "\n");
                printMenu();
                //:)
                break;         
        }
    }
}