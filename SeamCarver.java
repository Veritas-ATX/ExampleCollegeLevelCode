/******************************************************************************
 * Name: Austin Stiefelmaier   
 * NetID: ajcs  
 * Precept: P01
 *
 * Partner Name:    N/A
 * Partner NetID:   N/A
 * Partner Precept: N/A
 * 
 * Description: This program removes seams from a given Picture in order to 
 * facilitate image resizing while keeping relevant parts of the image. The 
 * constructor takes in a Picture and creates a defensive copy, gets its width
 * and height, and creates an energy matrix for each pixel. picture() returns
 * a different copy of the current Picture in SeamCarver, height() returns the
 * current Picture height, and width() returns the current picture width. 
 * energy returns the energy of the pixel at x,y. findHorizontalSeam() returns 
 * an array representation of the minimum energy horizontal seam. 
 * findVerticalSeam() returns an array representation of the minimum energy 
 * vertical seam. removeHorizontalSeam() removes the horizontal seam represented 
 * by the given array. removeVerticalSeam() removes the vertical seam 
 * represented by the given array. energySquare() is a helper method that 
 * calculates the square of the energy of a pixel. adjacentColor() returns the 
 * Color of a pixel and handles wrap-around. gradient() calculates the half of
 * the energy of a pixel. partialEnergies() populates a 2D array of the partial
 * energies of each pixel, and is used for finding minimum energy paths. 
 * isValidSeam() is used to determine if a given seam satisifes all of the rules
 * for it to be valid. transpose() transposes the energy matrix, the Picture, 
 * and W and H. The main() method serves as a tester. 
 * 
 ******************************************************************************/
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.Picture;
import java.awt.Color;

public class SeamCarver {
    // the height of the image
    private int H;
    // the width of the image
    private int W;
    // the defensive copy of the Picture
    private Picture pic;
    // the 2D energy matrix
    private double[][] energy;
    
    // create a seam carver object based on the given picture
    public SeamCarver(Picture picture) {
        if (picture == null) {
            throw new java.lang.NullPointerException();
        }
        pic = new Picture(picture);
        H = pic.height();
        W = pic.width();
        energy = new double[H][W];
        for (int y = 0; y < H; y++) {
            for (int x = 0; x < W; x++) {
                energy[y][x] = energySquare(x, y);
            }
        }
    }
    
    // current picture
    public Picture picture() {
        Picture picture = new Picture(pic);
        return picture;
    }
    
    // width of current picture
    public int width() {
        return W;
    }
    
    // height of current picture
    public int height() {
        return H;
    }
    
    // energy of pixel at column x and row y
    public double energy(int x, int y) {
        if (x < 0 || y < 0 || x > W - 1 || y > H - 1) {
            throw new java.lang.IndexOutOfBoundsException();
        }
        return Math.sqrt(energy[y][x]);
    }
    
    // sequence of indices for horizontal seam
    public int[] findHorizontalSeam() {
        transpose();
        int[] seam = findVerticalSeam();
        transpose();
        return seam;
    }
    
    // sequence of indices for vertical seam
    public int[] findVerticalSeam() {
        int[] seam = new int[H];
        double[][] partial = partialEnergies();
        double min = Double.POSITIVE_INFINITY;
        int index = 0;
        for (int i = 0; i < W; i++) {
            if (partial[H - 1][i] < min) {
                min = partial[H - 1][i];
                index = i;
            } 
        }
        seam[H - 1] = index;
        for (int j = H - 2; j >= 0; j--) {
            int current = seam[j + 1];
            int best = current;
            double bestVal = partial[j][current];
            double temp;
            if (current != 0) {
                temp = partial[j][current - 1];
                if (temp < bestVal) {
                    best = current - 1;
                    bestVal = temp;
                }
            } 
            if (current != W - 1) {
                temp = partial[j][current + 1];
                if (temp < bestVal) {
                    best = current + 1;
                    bestVal = temp;
                }
            }
            temp = partial[j][current];
            if (temp < bestVal) {
                best = current;
            }
            seam[j] = best;
        }
        return seam;
    }
    
    // remove horizontal seam from current picture
    public void removeHorizontalSeam(int[] seam) {
        transpose();
        removeVerticalSeam(seam);
        transpose();
    }
    
    // remove vertical seam from current picture
    public void removeVerticalSeam(int[] seam) {
        isValidSeam(seam);
        Picture picture = new Picture(W - 1, H);
        double[][] newEnergy = new double[H][W - 1];
        for (int y = 0; y < H; y++) {
            int place = 0;
            for (int x = 0; x < W; x++) {
                if (seam[y] == x) {
                    continue;
                }
                picture.set(place, y, pic.get(x, y));
                newEnergy[y][place] = energy[y][x];
                place++;
            }
        }
        pic = picture;
        energy = newEnergy;
        W--;       
        for (int i = 0; i < seam.length; i++) {
            if (seam[i] == 0 || seam[i] == W) {
                energy[i][0] = energySquare(0, i);
                energy[i][W - 1] = energySquare(W - 1, i);
            } 
            else {
                energy[i][seam[i]] = energySquare(seam[i], i);
                energy[i][seam[i] - 1] = energySquare(seam[i] - 1, i);
            }
        }
    }
    
    // helper method for calculating energy
    private double energySquare(int x, int y) {
        Color left = adjacentColor(x - 1, y);
        Color right = adjacentColor(x + 1, y);
        Color up = adjacentColor(x, y - 1);
        Color down = adjacentColor(x, y + 1);
        double xgrad = gradient(left, right);
        double ygrad = gradient(up, down);
        return xgrad + ygrad;
    }
    
    // helper method for getting Color of an adjacent pixel, with wrap-around
    private Color adjacentColor(int x, int y) {
        if (x < 0)
            x = W - 1;
        if (x > W - 1)
            x = 0;
        if (y < 0)
            y = H - 1;
        if (y > H - 1)
            y = 0;
        Color temp = pic.get(x, y);
        return temp;
    }
    
    // helper method for getting gradient values for energy
    private double gradient(Color first, Color second) {
        double grad = Math.pow(second.getBlue() - first.getBlue(), 2);
        grad += Math.pow(second.getGreen() - first.getGreen(), 2);
        grad += Math.pow(second.getRed() - first.getRed(), 2);
        return grad;
    }
    
    // helper method that creates the partial energies matrix
    private double[][] partialEnergies() {
        double[][] partial = new double[H][W];
        for (int y = 0; y < H; y++) {
            for (int x = 0; x < W; x++) {
                if (y == 0)
                    partial[y][x] = energy(x, y);
                else {
                    double min;
                    if (x == 0) {
                        if (W == 1)
                            min = partial[y - 1][x];
                        else {
                            min = Math.min(partial[y - 1][x], 
                                       partial[y - 1][x + 1]);
                        }
                        
                    } else
                        if (x == W - 1) {
                        min = Math.min(partial[y - 1][x], 
                                       partial[y - 1][x - 1]);
                    }
                    else
                        min = Math.min(Math.min(partial[y - 1][x], 
                                       partial[y - 1][x - 1]), 
                                       partial[y - 1][x + 1]);
                    partial[y][x] = min + energy(x, y);
                }
            }
        }
        return partial;
    }
    
    // checks seam validity
    private void isValidSeam(int[] seam) {
        if (seam == null) {
            throw new java.lang.NullPointerException();
        }
        if (W == 1) {
            throw new java.lang.IllegalArgumentException();
        }
        if (seam.length != H) {
            throw new java.lang.IllegalArgumentException();
        }
        int previous = seam[0];
        for (int i = 0; i < H; i++) {
            int diff = Math.abs(previous - seam[i]);
            if (seam[i] < 0 || seam[i] > W - 1 || diff > 1)
                throw new java.lang.IllegalArgumentException();
            previous = seam[i];
        }
    }
    
    // helper method to transpose
    private void transpose() {
        double[][] transEnergy = new double[W][H];
        Picture picture = new Picture(H, W);
        for (int y = 0; y < H; y++) {
            for (int x = 0; x < W; x++) {
                transEnergy[x][y] = energy[y][x];
                picture.set(y, x, pic.get(x, y));
            }
        }
        int temp = W;
        W = H;
        H = temp;
        energy = transEnergy;
        pic = picture;
    }
    
    // do unit testing of this class
    public static void main(String[] args) {
        Picture picture = new Picture("6x5.png");
        SeamCarver sc = new SeamCarver(picture);
        StdOut.println("Testing picture(): " + picture.equals(sc.picture()));
        StdOut.println("Testing height(): " + (sc.height() == 5));
        StdOut.println("Testing width(): " + (sc.width() == 6));
        StdOut.println("Testing energy(): " + 
                       (Math.floor(sc.energy(0, 0)) == 240.0));
        int[] a = sc.findVerticalSeam();
        StdOut.println("Testing findVerticalSeam(): want 3,4,3,2,2");
        for (int i = 0; i < a.length; i++) {
            StdOut.print(a[i] + " ");
        }
        StdOut.println();
        int[] b = sc.findHorizontalSeam();
        StdOut.println("Testing findHorizontalSeam(): want 2,2,1,2,1,2");
        for (int i = 0; i < b.length; i++) {
            StdOut.print(b[i] + " ");
        }
        StdOut.println();
        sc.removeVerticalSeam(a);
        int[] c = sc.findHorizontalSeam();
        sc.removeHorizontalSeam(c);
    }
}