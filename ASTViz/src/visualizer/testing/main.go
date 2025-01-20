package main

import (
	"fmt"
	"html/template"
	"net/http"
	"net"
	"log"
	"os"
	"strconv"
	"os/exec"
	"strings"
	"github.com/gin-contrib/static"
	_ "github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	host := GetLocalIP()
	if len(os.Args) != 2 {
		log.Fatal("Please provide exactly one argument for the port number")
	}
	port := os.Args[1]
	if isValidPort(port) {
		fmt.Printf("Port %s is valid.\n", port)
	} else {
		log.Fatalf("Port %s is not valid. Please provide a port number between 1 and 65535.\n", port)
	}

	r.GET("/", func(c *gin.Context) {
		tmpl, _ := template.ParseFiles("./static/index.html")
		data := gin.H{
			"Host": host,
			"Port": port,
		}
		tmpl.Execute(c.Writer, data)
	})
	r.Use(static.Serve("/",static.LocalFile("./static", true)))
	r.POST("/api/root", RootDisplay)
	r.POST("/api/node", NodeDisplay)
	r.Run(":"+port+"") // Run the server on port 9000
}

func NodeDisplay(c *gin.Context) {
	nameidbranch := c.PostForm("nameid")
	var nameid string
	fmt.Println(nameidbranch)
	parts := strings.Split(nameidbranch, "-")
	if len(parts) >= 2 {
		nameid = parts[0] + "-" + parts[1]
	}
	exist := FindTheFile(nameid) //Function call to find if the file exist in the json_split_output directory or not
	fmt.Println("The File exist or not")
	fmt.Println(exist)
	if exist != false {
		listoffiles := ListOfFiles(nameid) //Function call to get the list of files
		fmt.Println(listoffiles)
		copyjsondata := CopyJsonData(nameidbranch + "json") //Function call to copy the json data to the file json.json
		fmt.Println(copyjsondata)
		c.JSON(http.StatusOK, gin.H{"listoffiles": listoffiles})
	}
}

func RootDisplay(c *gin.Context) {
	nodenamenodeid := c.PostForm("nameid")
	exist := FindTheFile(nodenamenodeid) //Function call to find if the file exist in the json_split_output directory or not
	fmt.Println("The File exist or not")
	fmt.Println(exist)
	if exist != false {
		listoffiles := ListOfFiles(nodenamenodeid) //Function call to get the list of files
		fmt.Println(listoffiles)
		copyjsondata := CopyJsonData(listoffiles[0] + "json") //Function call to copy the json data to the file json.json
		fmt.Println(copyjsondata)
		c.JSON(http.StatusOK, gin.H{"listoffiles": listoffiles})
	}
}

// Function to copy the json data to the file json.json
func CopyJsonData(nameidbranch string) bool {

	filenm := exec.Command("bash", "-c", "cat ./json_split_output/"+nameidbranch+".json > ../jsontree/json.json;")
	_, err := filenm.CombinedOutput()
	if err != nil {
		//fmt.Printf("Error running the command: %s\n", err)
		return false
	}
	//fmt.Printf("Command output:\n%s\n", boolean)
	return true

}

// Function to get the list of files
func ListOfFiles(nameid string) []string {

	var listfile []string

	listofnode := exec.Command("bash", "-c", "cd ./json_split_output;ls *"+nameid+"*;")
	list, _ := listofnode.CombinedOutput()
	splitdata := strings.Split(string(list), "\n")
	for _, file := range splitdata {
		if file != "" {
			filename := strings.Split(file, ".")[0]
			listfile = append(listfile, filename)
		}
	}

	return listfile

}

// Function to find if the file exist in the json_split_output directory or not
func FindTheFile(nameid string) bool {

	fmt.Println(nameid)
	boolea := exec.Command("bash", "-c", "cd ./json_split_output;ls *"+nameid+"*;")
	_, err := boolea.CombinedOutput()
	if err != nil {
		fmt.Printf("Error running the command: %s\n", err)
		return false
	}
	//fmt.Printf("Command output:\n%s\n", boolean)
	return true

}

// config := cors.DefaultConfig()
// config.AllowOrigins = []string{"http://172.29.42.165:7774"}              // List of allowed origins
// config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"} // List of allowed HTTP methods
// r.Use(cors.New(config))

func GetLocalIP() string {
    addrs, err := net.InterfaceAddrs()
    if err != nil {
        return ""
    }
    for _, address := range addrs {
        // check the address type and if it is not a loopback the display it
        if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
            if ipnet.IP.To4() != nil {
                return ipnet.IP.String()
            }
        }
    }
    return ""
}

func isValidPort(port string) bool {
	// Convert the port to an integer
	portInt, err := strconv.Atoi(port)
	if err != nil {
		return false
	}
	// Check if the port is within the valid range
	return portInt >= 1 && portInt <= 65535
}
