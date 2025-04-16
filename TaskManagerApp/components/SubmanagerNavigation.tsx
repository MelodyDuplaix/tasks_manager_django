import { Text, View, StyleSheet, TouchableOpacity } from "react-native";
import { useRouter } from 'expo-router';

interface SubmanagerNavigationProps {
  submanagers: any[];
  submanagerId: number;
  submanagerName: string;
}

const SubmanagerNavigation: React.FC<SubmanagerNavigationProps> = ({ submanagers, submanagerId, submanagerName }) => {
  const router = useRouter();

  const getPreviousSubmanager = () => {
    const currentIndex = submanagers.findIndex(sm => sm.id === submanagerId);
    if (currentIndex > 0) {
      return submanagers[currentIndex - 1];
    } else if (submanagers.length > 1) {
      return submanagers[submanagers.length - 1];
    }
    return null;
  };

  const getNextSubmanager = () => {
    const currentIndex = submanagers.findIndex(sm => sm.id === submanagerId);
    if (currentIndex < submanagers.length - 1) {
      return submanagers[currentIndex + 1];
    } else if (submanagers.length > 1) {
      return submanagers[0];
    }
    return null;
  };

  const renderNavigationButtons = () => {
    if (submanagers.length === 2) {
      const nextSubmanager = getNextSubmanager();
      return (
        nextSubmanager && (
          <TouchableOpacity
            style={styles.navButton}
            onPress={() => {
              router.replace(`/submanager/${nextSubmanager.id}`);
            }}
          >
            <Text style={styles.navButtonText}>{nextSubmanager.name}</Text>
          </TouchableOpacity>
        )
      );
    } else if (submanagers.length > 2) {
      const previousSubmanager = getPreviousSubmanager();
      const nextSubmanager = getNextSubmanager();
      return (
        <>
          {previousSubmanager && (
            <TouchableOpacity
              style={styles.navButton}
              onPress={() => {
                router.replace(`/submanager/${previousSubmanager.id}`);
              }}
            >
              <Text style={styles.navButtonText}>{previousSubmanager.name}</Text>
            </TouchableOpacity>
          )}
          {nextSubmanager && (
            <TouchableOpacity
              style={styles.navButton}
              onPress={() => {
                router.replace(`/submanager/${nextSubmanager.id}`);
              }}
            >
              <Text style={styles.navButtonText}>{nextSubmanager.name}</Text>
            </TouchableOpacity>
          )}
        </>
      );
    }
    return null;
  };

  return (
    <View style={styles.titleContainer}>
      {getPreviousSubmanager() && submanagers.length > 2 && (
        <TouchableOpacity
          style={styles.navButton}
          onPress={() => {
            router.replace(`/submanager/${getPreviousSubmanager().id}`);
          }}
        >
          <Text style={styles.navButtonText}>{getPreviousSubmanager()?.name}</Text>
        </TouchableOpacity>
      )}
      <Text style={styles.title}>{submanagerName}</Text>
      {getNextSubmanager() && submanagers.length > 2 && (
        <TouchableOpacity
          style={styles.navButton}
          onPress={() => {
            router.replace(`/submanager/${getNextSubmanager().id}`);
          }}
        >
          <Text style={styles.navButtonText}>{getNextSubmanager()?.name}</Text>
        </TouchableOpacity>
      )}
      {submanagers.length === 2 && renderNavigationButtons()}
    </View>
  );
};

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
  },
  navButton: {
    backgroundColor: '#ddd',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  navButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
});

export default SubmanagerNavigation;
